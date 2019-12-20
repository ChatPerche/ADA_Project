
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



NaN_Mask_Value                = 0
underflow_buffer              = 0
default_dense_layers          = 0
default_model_complexity      = 20
default_batch_size            = 1
default_num_epochs            = 1
default_train_test_ratio      = 0.90
default_learning_rate         = 0.0001
default_nan_percent_cutoff    = 0.33
default_shap_samples          = 20
default_dense_activation      = tf.sigmoid
default_output_activation     = None

default_input_scaling         = None
default_include_t0            = True
default_include_output_column = False


def reshape_and_pad(data, time_series_length, columns,
                    verbose = False,
                    differentiate=True):
    """
    Takes data from database format. Reshapes into sets of differentied timeseries,
    with one set of timeseries per country and start year. Missing values are padded

    :param data: Data in database format
    :param time_series_length: The number of data points used per differentiated time series.
            It will be one more than the length of the number of elements contained per
            differentiated time series.
    :param columns: A list of (element_code, item_code) pairs to choose which
            indicates the time series to extract
    :param verbose: Silences prints if set to False
    :param differentiate:
    :return: A list of samples, one for each (country code, timeseries_start_year)
            pair. Each sample contains the padded timeseries selected by the columns parameter
    """

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
                if not any(slice.index.isin([(area_c,year)])):
                    new_row =  pd.Series([np.nan for i in range(len(columns))]+[year,area_c],
                                  index = slice.columns,name=(area_c,year))
                    slice = slice.append(new_row)

        # Consider values with 0 as NaNs
        slice = slice.replace(to_replace=0,value=np.nan)
        slice = slice.sort_index()


        if differentiate:
            # Introducing differentiation - values are on a scale of ]-1,+inf[
            to_diff = slice[slice.columns[:-2].values]
            slice[slice.columns[:-2].values] = (to_diff-to_diff.shift())/to_diff

        for area_c in area_codes:

            to_append = slice[slice.areacode_copy == area_c] \
                .replace(to_replace=[-np.inf, np.inf, np.nan], value=NaN_Mask_Value) \
                .mask(slice <= -1 + underflow_buffer, NaN_Mask_Value) \
                .drop(columns='year_copy')\

            if differentiate:
                to_append = to_append.drop(labels=start_year, level=1)

            to_append = to_append.drop(columns='areacode_copy')

            observations.append(to_append)

    return observations

def filter_samples(observations,
                   ratio                 = default_train_test_ratio,
                   batch_size            = default_batch_size,
                   include_output_column = default_include_output_column,
                   include_t0            = default_include_t0,
                   nan_percent_cutoff    = default_nan_percent_cutoff,
                   input_scaling         = default_input_scaling,
                   custom_filtering      = None,
                   should_shuffle        = True,
                   verbose               = False):

    def nan_percent_thresholding(df):

        if len(df.columns) is 1:
            value_counts = df.stack().value_counts(normalize=True)
        else:
            value_counts = df[df.columns[:-1]].stack().value_counts(normalize=True)

        return    (not (NaN_Mask_Value in value_counts.index)) \
               or (value_counts.loc[NaN_Mask_Value] <= nan_percent_cutoff )

    assert(not (include_output_column and include_t0))

    if verbose:
        print('Non Filtered Samples: ', len(observations))

    select_input_rows    = lambda df: df if include_t0 else df.iloc[:-1]
    select_input_columns = lambda df: df if (include_output_column or len(df.columns) is 1) \
                                         else df[df.columns[:-1]]
    select_input         = lambda df: select_input_columns(select_input_rows(df))
    select_ouput         = lambda df: df.iloc[-1:][df.columns[-1:]]

    input_output_is_all_nan = lambda df: (np.all((select_input(df).values == NaN_Mask_Value)) \
                                        or select_ouput(df).values[0][0] == NaN_Mask_Value )

    keep_slice = lambda df : (( not input_output_is_all_nan(df))
                  and ( nan_percent_thresholding(df) if nan_percent_cutoff is not None else True)
                  and ( custom_filtering(df) if custom_filtering is not None else True))

    shuffled = observations
    if should_shuffle:
        shuffle(shuffled)

    ratio    = int(len(shuffled)*ratio)
    train    = shuffled[:ratio]
    test     = shuffled[ratio:]

    shorten_to_batch = lambda x: np.array(x[:int(len(x) / batch_size) * batch_size])

    test_Y   = shorten_to_batch([select_ouput(df).values for df in test  if keep_slice(df)])
    train_Y  = shorten_to_batch([select_ouput(df).values for df in train if keep_slice(df)])
    test_X   = shorten_to_batch([select_input(df).values for df in test  if keep_slice(df)])
    train_X  = shorten_to_batch([select_input(df).values for df in train if keep_slice(df)])

    if verbose:
        print('Filtered Training Samples:'  , len(train_X),
              ' / Filtered Testing Samples:', len(train_Y))

    if input_scaling is None:
        input_scaling = lambda x : x

    return input_scaling(train_X), train_Y, input_scaling(test_X), test_Y

def build_lstm(num_input_timeseries, num_timesteps,
              model_complexity           = default_model_complexity,
              batch_size                 = default_batch_size,
              dense_layer_activation     = default_dense_activation,
              output_layer_activation    = default_output_activation,
              num_dense_layers           = default_dense_layers,
              verbose=False):
    '''
    Builds LSTM model 
    :param num_input_timeseries: The number of timeseries used as input
    :param num_timesteps: The number of elements per timeseries
    :param model_complexity: Influences the width of our network 
    :param batch_size: The size of each batch during training
    :param output_layer_activation:
    :param dense_layer_activation:
    :param num_dense_layers:
    :param verbose: Silences prints if set to False
    :return: An untrained model object
    '''


    model = k.Sequential()

    model.add(k.layers.InputLayer(input_shape =(num_timesteps,num_input_timeseries),
                                  batch_size=batch_size))

    model.add(k.layers.Masking(mask_value=NaN_Mask_Value))

    model.add(k.layers.LSTM(int(model_complexity),stateful=False,
                            name='lstm_1'))

    model.add(k.layers.RepeatVector(1))

    model.add(k.layers.LSTM(int(model_complexity),stateful=False, return_sequences=False,
                             name='lstm_2'))

    for i in range(num_dense_layers,0,-1):
        model.add(k.layers.Dense(model_complexity * i / float(num_dense_layers),
                                 activation=dense_layer_activation))
        model.add(k.layers.Dropout(0.33))

    model.add(k.layers.Dense(1, activation=output_layer_activation))

    if verbose:
        print(model.summary())

    return model

def build_and_run_lstm(train_X, train_Y, test_X, test_Y,
             model_complexity            = default_model_complexity,
             batch_size                  = default_batch_size,
             num_epochs                  = default_num_epochs,
             learning_rate               = default_learning_rate,
             dense_layer_activation      = default_dense_activation,
             output_layer_activation     = default_output_activation,
             num_dense_layers            = default_dense_layers,
             verbose                     = False):

    """
    Builds and trains LSTM model 
    :param train_X: Numpy 3D array with dimensions ( # samples, # timesteps, # features ) - Scaled 
    :param train_Y: Numpy 3D array with dimensions ( # samples, # timesteps, # features ) - Scaled 
    :param test_X:  Numpy 3D array with dimensions ( # samples, 1, 1 ) - Scaled 
    :param test_Y:  Numpy 3D array with dimensions ( # samples, 1, 1 ) - Scaled 
    :param model_complexity: Influences the width of our network 
    :param batch_size: The size of each batch during training
    :param num_epochs: The number of epochs to train for
    :param learning_rate: The learning rate passed to our optimizer
    :param dense_layer_activation:
    :param output_layer_activation:
    :param num_dense_layers:
    :param verbose: Silences prints if set to False
    :return: Returns both the trained model, and its associated history object
    """

    def adj_loss(y_true, y_pred):

        """
        Custom Loss Function for Tensorflow model
        :param y_true: Batch Ground Truth - Scaled 
        :param y_pred: Batch output - Scaled 
        :return: MSE error of batch, as measured with respect to our descaled values
        """
        return ((y_pred-y_true)/(1+y_true))**2

    def rms(y_true,y_pred):
        return tf.sqrt(adj_loss(y_true,y_pred))

    model = build_lstm(num_input_timeseries    = train_X[0].shape[1],
                       num_timesteps           = train_X[0].shape[0],
                       model_complexity        = model_complexity,
                       batch_size              = batch_size,
                       num_dense_layers        = num_dense_layers,
                       output_layer_activation = output_layer_activation,
                       dense_layer_activation  = dense_layer_activation)

    model.compile(optimizer=k.optimizers.Adam(lr=learning_rate),loss=k.losses.MAE,metrics=[rms])

    training_set = tf.data.Dataset.from_tensor_slices((
        tf.cast(train_X, tf.float32),
        tf.cast(train_Y.reshape(-1,1), tf.float32))).batch(batch_size).shuffle(batch_size*2)

    testing_set = tf.data.Dataset.from_tensor_slices((
        tf.cast(test_X, tf.float32),
        tf.cast(test_Y.reshape(-1,1), tf.float32))).batch(batch_size).shuffle(batch_size*2)


    history = model.fit(training_set, validation_data=testing_set,
                        epochs=num_epochs, verbose=1 if verbose else 0, shuffle=False)

    return model, history

def calculate_shap_values(data,max_lag_steps,input_columns,output_columns,
                  include_output_column  = default_include_output_column,
                  include_t0             = default_include_t0,
                  model_complexity       = default_model_complexity,
                  batch_size             = default_batch_size,
                  num_epochs             = default_num_epochs,
                  learning_rate          = default_learning_rate,
                  num_dense_layers       = default_dense_layers,
                  dense_layer_activation = default_dense_activation,
                  output_layer_activation= default_output_activation,
                  input_scaling          = default_input_scaling,
                  num_shap_samples       = default_shap_samples,
                  nan_percent_cutoff     = default_nan_percent_cutoff,
                  verbose                = False):

    assert(not (include_output_column and include_t0))
    assert(len(output_columns)== 1)
    assert(max_lag_steps>=1)

    time_series_length               = max_lag_steps if include_t0 else max_lag_steps + 1


    samples                          = reshape_and_pad(data, time_series_length,
                                                       input_columns+output_columns,
                                                       verbose=verbose)

    train_X, train_Y, test_X, test_Y = filter_samples(samples,
                                                include_output_column  = include_output_column,
                                                include_t0             = include_t0,
                                                input_scaling          = input_scaling,
                                                nan_percent_cutoff     = nan_percent_cutoff,
                                                verbose                = verbose )


    model, history                   = build_and_run_lstm(train_X, train_Y, test_X, test_Y,
                                                model_complexity        = model_complexity,
                                                batch_size              = batch_size,
                                                num_epochs              = num_epochs,
                                                learning_rate           = learning_rate,
                                                num_dense_layers        = num_dense_layers,
                                                dense_layer_activation  = dense_layer_activation,
                                                output_layer_activation = output_layer_activation,
                                                verbose                 = verbose)

    if verbose:
        print("Validation losses:", history.history['val_loss'][-1],
              " / Training losses:", history.history['loss'][-1],
              " Test Y std_dev:", np.std(test_Y) )


    input_reshape = lambda x : np.reshape(x,(1, time_series_length - 1, len(input_columns)))
    f             = lambda X : np.array([model.predict(input_reshape(x)) for x in X])

    flattened_X   = np.reshape(train_X[:num_shap_samples], (-1,train_X.shape[1]*train_X.shape[2]))

    kernel_explainer   = shap.KernelExplainer(f, flattened_X)
    lookup_elem        = lambda elem_c : data[data.elementcode == elem_c].element.tolist()[0]
    lookup_item        = lambda item_c : data[data.itemcode == item_c].item.tolist()[0]

    feature_names = [lookup_elem(element_c)+'/'+ lookup_item(item_c)+" : t-"+            \
                     str(i-1 if include_t0 else i) for i in range(max_lag_steps-1,0,-1)  \
                                                   for element_c, item_c in input_columns ]



    return lambda : shap.summary_plot(kernel_explainer.shap_values(flattened_X),
                                        flattened_X,feature_names)
