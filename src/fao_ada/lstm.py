
from random import shuffle
import pandas as pd
import pydot, sys
import tensorflow as tf
import tensorflow.keras as k
import numpy as np
import shap

# For shap library :
# pip install git+git://github.com/AndreCNF/shap@master
# Specific fork needed -- pulled from repository on December 10th

# Necessary for tf.keras.layers.Masking as checking for np.nan equality doesn't work
# depending on hardware environment
NaN_Mask_Value   = -1 #-100
underflow_buffer = 0

default_model_complexity = 200
default_batch_size       = 10
default_num_epochs       = 1000
default_train_test_ratio = 0.80
default_learning_rate    = 0.001


def reshape_and_pad(data, time_series_length, columns,
                    verbose = False, differentiate=True, for_model=True):
    '''
    Takes data from database format. Reshapes into sets of differentied timeseries,
    with one set of timeseries per country and start year. Missing values are padded

    :param data: Data in database format
    :param time_series_length: The number of data points used per differentiated time series.
            It will be one more than the length of the number of elements contained per
            differentiated time series.
    :param columns: A list of (element_code, item_code) pairs to choose which
            indicates the time series to extract
    :param verbose: Silences prints if set to False
    :return: A list of samples, one for each (country code, timeseries_start_year)
            pair. Each sample contains the padded timeseries selected by the columns parameter
    '''

    # We start by reshaping into a format with (element_code, item_code) pairs as columns
    #  and with (year,country) pairs as columns. reshaped_data will be the resulting dataframe.
    reshaped_data = None

    for element_c, item_c in columns:

        # One slice is the unordered collection of samples from the union of the all timeseries
        #   with a given (element_code, item_code) pair
        column_name = 'i: '+str(item_c)+" / e: "+str(element_c)
        slice       = data[(data.itemcode == item_c) & (data.elementcode == element_c)]\
                          [['areacode','year','value']]

        column_dict = dict(zip(list(slice.columns.values),['areacode','year', column_name]))
        slice       = slice.rename(columns=column_dict)

        # Check integrity, and overlapping values
        slice = slice.set_index(['areacode','year'],verify_integrity=True)

        # If even a single data point exists for a given (area_code, year),
        #  the missing values across all selected (element_code,item_code) pairs

        #  for that given area_code and year will be replaced with NaNs ( because of outer merge )
        #
        #  NaNs are kept here in order to keep track of the valid edges of each
        #    time series. This will be useful when we populate our list of observations
        if reshaped_data is not None:
            reshaped_data = pd.merge(reshaped_data,slice,how='outer',
                                     left_index=True,right_index=True)
        else:
            reshaped_data = slice

    # From our reshaped data, we then create a list of samples, one for each
    #      (country code, timeseries_start_year pair)
    observations  = []

    area_codes    = reshaped_data.index.get_level_values(0).unique().values
    year_idxs     = sorted(reshaped_data.index.get_level_values(1).unique().values)[:-7]
    reshaped_data['year_copy']     = reshaped_data.index.get_level_values(1).astype(int)
    reshaped_data['areacode_copy'] = reshaped_data.index.get_level_values(0).astype(int)

    if verbose :
        print("Year range studied : ",str(year_idxs[0])," - ",str(year_idxs[-1]))

    for start_year in range(year_idxs[0], year_idxs[-1] - time_series_length):

        if verbose:
            print("Processing year: ",start_year)

        # One slice is a set of time series for a given start year
        #   Each column of the slice is a time series
        slice = reshaped_data[(reshaped_data.year_copy >= start_year) &
                  (reshaped_data.year_copy < (start_year + time_series_length))]


        # Pad missing values with NaNs.
        for year in range(start_year,start_year+time_series_length):
            for area_c in area_codes:
                if (area_c,year) not in slice.index.values:
                    new_row =  pd.Series([np.nan for i in range(len(columns))]+[year,area_c],
                                  index = slice.columns,name=(area_c,year))
                    slice.append(new_row)

        # Consider values with 0 as NaNs
        slice = slice.replace(to_replace=0,value=np.nan)
        slice = slice.sort_index()


        if differentiate:
            # Introducing differentiation - values are on a scale of ]-1,+inf[
            # Apply tanh scaling - values are on a scale of ]tanh(-1),1[
            to_differentiate = slice[slice.columns[:-2].values]
            slice[slice.columns[:-2].values] = (to_differentiate-to_differentiate.shift())/to_differentiate

        for area_c in area_codes:

            to_append = slice[slice.areacode_copy == area_c] \
                .replace(to_replace=[-np.inf, np.inf, np.nan, 0], value=NaN_Mask_Value) \
                .mask(slice <= -1 + underflow_buffer, NaN_Mask_Value) \
                .drop(columns='year_copy').drop(labels=start_year, level=1) \
                .drop(columns='areacode_copy')



            if to_append.shape[0] == time_series_length - 1:

                observations.append(to_append)


    return observations

def filter_samples(observations,
                   ratio=default_train_test_ratio,
                   include_output_column =False,
                   include_t0 = False,
                   for_model  = True,
                   nan_percent_cutoff = None,
                   custom_filtering = None,
                   input_scaling = None):

    def nan_percent_thresholding(df):
        value_counts=None
        if len(df.columns) is 1:
            value_counts = df.stack().value_counts(normalize=True)
        else:
            value_counts = df[df.columns[:-1]].stack().value_counts(normalize=True)
        return (not -NaN_Mask_Value in value_counts.index) or (value_counts.loc[NaN_Mask_Value] < nan_percent_cutoff )

    assert(not (include_output_column and include_t0))

    select_input_rows    = lambda df: df if include_t0 else df.iloc[:-1]
    select_input_columns = lambda df: df if (include_output_column or len(df.columns) is 1) \
                                         else df[df.columns[:-1]]
    select_input         = lambda df: select_input_columns(select_input_rows(df))
    select_ouput         = lambda df: df.iloc[-1:][df.columns[-1:]]

    input_output_is_all_nan = lambda df: np.all((select_input(df).values == NaN_Mask_Value)) \
                                        or select_ouput(df).values[0][0] == NaN_Mask_Value
    keep_slice = lambda df : ( not input_output_is_all_nan(df) if for_model else True ) \
                         and ( nan_percent_thresholding(df) if nan_percent_cutoff is not None else True)\
                         and ( custom_filtering(df) if custom_filtering is not None else True)

    #shuffle(observations)

    train    = observations[:int(len(observations)*ratio)]
    test     = observations[int(len(observations)*ratio):]
    test_Y   = np.array([select_ouput(df).values for df in test  if keep_slice(df)])
    train_Y  = np.array([select_ouput(df).values for df in train if keep_slice(df)])
    test_X   = np.stack([select_input(df).values for df in test  if keep_slice(df)],axis=0)
    train_X  = np.stack([select_input(df).values for df in train if keep_slice(df)],axis=0)

    if input_scaling is None:
        input_scaling = lambda x : x
    return input_scaling(train_X), train_Y, input_scaling(test_X), test_Y

def build_lstm(num_input_timeseries, num_timesteps,
              model_complexity=default_model_complexity,
              batch_size=default_batch_size,
              dense_layer_activation=tf.sigmoid,
              ouput_layer_activation=None,
              num_dense_layers = 15,
              verbose=False):
    '''
    Builds LSTM model 
    :param num_input_timeseries: The number of timeseries used as input
    :param num_timesteps: The number of elements per timeseries
    :param model_complexity: Influences the width of our network 
    :param batch_size: The size of each batch during training
    :param verbose: Silences prints if set to False
    :return: An untrained model object
    '''


    print(num_timesteps,num_input_timeseries)

    model = k.Sequential()

    model.add(k.layers.InputLayer(input_shape =(num_timesteps,num_input_timeseries),
                                  batch_size=batch_size))

    model.add(k.layers.Masking(mask_value=NaN_Mask_Value))

    model.add(k.layers.LSTM(int(model_complexity),stateful=True,name='lstm_1'))

    model.add(k.layers.RepeatVector(1))

    model.add(k.layers.LSTM(int(model_complexity),stateful=True, return_sequences=True,
                            name='lstm_2'))
    model.add(k.layers.LSTM(int(model_complexity),stateful=True, return_sequences=True,
                            name='lstm_3'))

    for i in range(num_dense_layers,0,-1):
        model.add(k.layers.Dense(model_complexity * i / float(num_dense_layers),
                                 activation=dense_layer_activation))
        model.add(k.layers.Dropout(0.1))

    model.add(k.layers.Dense(1, activation=ouput_layer_activation))

    if verbose:
        print(model.summary())


    return model

def build_and_run_lstm(train_X, train_Y, test_X, test_Y,
             model_complexity=default_model_complexity,
             batch_size=default_batch_size,
             num_epochs=default_num_epochs,
             learning_rate=default_learning_rate,
             verbose=False):

    '''
    Builds and trains LSTM model 
    :param train_X: Numpy 3D array with dimensions ( # samples, # timesteps, # features ) - Scaled 
    :param train_Y: Numpy 3D array with dimensions ( # samples, # timesteps, # features ) - Scaled 
    :param test_X:  Numpy 3D array with dimensions ( # samples, 1, 1 ) - Scaled 
    :param test_Y:  Numpy 3D array with dimensions ( # samples, 1, 1 ) - Scaled 
    :param model_complexity: Influences the width of our network 
    :param batch_size: The size of each batch during training
    :param num_epochs: The number of epochs to train for
    :param learning_rate: The learning rate passed to our optimizer
    :param verbose: Silences prints if set to False
    :return: Returns both the trained model, and its associated history object
    '''

    def adj_loss(y_true, y_pred):

        '''
        Custom Loss Function for Tensorflow model
        :param y_true: Batch Ground Truth - Scaled 
        :param y_pred: Batch output - Scaled 
        :return: MSE error of batch, as measured with respect to our descaled values
        '''
        return (y_pred-y_true)**2

    def rms(y_true,y_pred):
        return tf.sqrt(adj_loss(y_true,y_pred))

    model = build_lstm(num_input_timeseries=train_X[0].shape[1],
                       num_timesteps=train_X[0].shape[0],
                       model_complexity=model_complexity,
                       batch_size=batch_size,verbose=verbose)

    model.compile(optimizer=k.optimizers.Adam(lr=learning_rate),loss=k.losses.MSE,metrics=[rms])

    training_set = tf.data.Dataset.from_tensor_slices(( \
        tf.cast(train_X, tf.float32), \
        tf.cast(train_Y, tf.float32))).batch(batch_size).shuffle(batch_size*2)

    testing_set = tf.data.Dataset.from_tensor_slices((
        tf.cast(test_X, tf.float32),
        tf.cast(test_Y, tf.float32))).batch(batch_size).shuffle(batch_size*2)

    print(train_X.shape,train_Y.shape)
    print(testing_set)



    history = model.fit(training_set, validation_data=testing_set,
                        epochs=num_epochs, verbose=1 if verbose else 0, shuffle=False)

    return model, history

def calculate_shap_values(data,max_lag_steps,input_columns,output_columns,
                  include_output_column = False,
                  include_t0 = False,
                  model_complexity=default_model_complexity,
                  batch_size=default_batch_size,
                  num_epochs=default_num_epochs,
                  learning_rate=default_learning_rate,
                  custom_X = None,
                  verbose = False):

    assert(not (include_output_column and include_t0))
    assert(len(output_columns)== 1)
    assert(max_lag_steps>=1)

    num_input_columns                = len(input_columns) if not include_output_column \
                                                                    else len(input_columns)+1
    time_series_length               = max_lag_steps if include_t0 else max_lag_steps + 1
    samples                          = reshape_and_pad(data, time_series_length,
                                                       input_columns+output_columns)
    train_X, train_Y, test_X, test_Y = filter_samples(samples,
                                                include_output_column=include_output_column,
                                                include_t0 = include_t0)
    print(train_X[0])

    model, history                   = build_and_run_lstm(train_X, train_Y, test_X, test_Y,
                                                model_complexity=model_complexity,
                                                batch_size=batch_size,num_epochs=num_epochs,
                                                learning_rate=learning_rate,verbose=verbose)

    print("Number of training samples: ", len(samples))
    print("Validation losses:", history.history['val_loss'][-1],
          " / Training losses:", history.history['loss'][-1] )

    if custom_X is None:
        custom_X = test_X

    f                  = lambda x: model.predict(np.reshape(x, (x.shape[0], max_lag_steps-1, num_input_columns)))
    flattened_test     = np.reshape(custom_X, (custom_X.shape[0], custom_X.shape[1] * custom_X.shape[2]))
    kernel_explainer   = shap.KernelExplainer(f, flattened_test)
    kernel_shap_values = kernel_explainer.shap_values(flattened_test)

    return kernel_shap_values, custom_X

def plot_summary(kernel_shap_values,X,time_series_names,max_lag_steps,include_t0):

    feature_names = [str(element_c)+'/'+str(item_c)+" : t-"+str(i-1 if include_t0  else i) \
        for i in range(max_lag_steps-1,0,-1) for element_c, item_c in time_series_names ]

    return shap.summary_plot(kernel_shap_values,X,feature_names)