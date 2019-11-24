import pandas as pd
import pydot
import tensorflow as tf
import tensorflow.keras as k
import sklearn as sk

from sklearn import preprocessing
import numpy as np

from random import shuffle

def introduce_differentiation(slice):
    return np.tanh((slice - slice.shift()).dropna(axis=0,how='all')/(slice.loc[1:]))

def build_samples(data, max_lag_steps, input_columns, output_columns):

    reshaped_data = None
    for element_c, item_c in input_columns + output_columns:

        # One slice is the unordered collection of samples
        #  from the union of the all timeseries with a given
        #   (element_code, item_code) pair
        column_name = 'i: '+str(item_c)+" / e: "+str(element_c)
        slice = data[data.itemcode == item_c][['areacode','year',str(element_c)]]

        slice = slice.rename(columns=dict(zip(list(slice.columns.values),
                                            ['areacode','year', column_name])))

        slice = slice.set_index(['areacode','year'])

        slice = introduce_differentiation(slice)

        slice[column_name] = preprocessing.MinMaxScaler(feature_range=(0, 1))\
                            .fit_transform(slice.values)


        # If even a single data point exists for a given (area_code, year),
        #  the missing values across all selected (element_code,item_code) pairs
        #  for that given area_code and year will be replaced with NaNs
        #
        #  NaNs are kept here in order to keep track of the valid edges of each
        #    time series. This will be useful when we populate our list of observations
        if reshaped_data is not None:
            reshaped_data = pd.merge(reshaped_data,slice,how='outer',
                                     left_index=True,right_index=True)
        else:
            reshaped_data = slice

    observations = []

    df = reshaped_data.reset_index()
    year_idxs = sorted(df.year.unique())[:-2]
    area_codes = df.areacode.unique()

    # max_lag_steps + 1 - 1
    for start_year in range(year_idxs[0], year_idxs[-1] - (max_lag_steps + 1 -1)):
        for area_c in area_codes:

            # One slice is a set of time series over an area
            #   Each column of the slice is a time series
            slice = df[(df.year >= start_year) &
                        (df.year < start_year + max_lag_steps + 1 -1 ) &
                        (df.areacode == area_c)].reset_index()

            # If do not have max_lag_steps+1 rows to our slice,
            #  this means that for a given (area_code, year)
            #  no data was available for any of the selected time series
            #  As such, we drop those slices.

            # Further filtering of observations based on
            #  window placement w.r.t the valid edges of the time series
            #  could be done here

            # The last condition checks that none of the values that we
            #   are trying to predict on are Nans
            if (not slice.isnull().values.any())  \
                and len(slice)==max_lag_steps+1 -1 \
                and not slice.iloc[:1][df.columns[-len(output_columns):]].isnull().values.any():
                observations.append(slice.fillna(0))

    return observations

def reshuffle_observations(observations,ratio,n_outputs):

    def stack_samples(samples):
        return np.rollaxis(np.dstack(samples),-1)

    shuffled = [obs.drop(['areacode','year','index'],axis=1) for obs in observations]
    shuffle(shuffled)

    train    = shuffled[:int(len(shuffled)*ratio)]
    test     = shuffled[int(len(shuffled)*ratio):]
    test_Y   = stack_samples([df.iloc[-1:][df.columns[-n_outputs:]].values for df in test])
    test_X   = stack_samples([df.iloc[:-1].values                          for df in test])
    train_Y  = stack_samples([df.iloc[-1:][df.columns[-n_outputs:]].values for df in train])
    train_X  = stack_samples([df.iloc[:-1].values                          for df in train])

    return train_X, train_Y, test_X, test_Y

def build_lstm(num_input_timeseries,num_output_dimensions,num_timesteps,model_complexity,batch_size):

    model = k.Sequential()

    model.add(k.layers.LSTM(model_complexity,
                            input_shape=(num_timesteps,num_input_timeseries),
                            unroll=False))
    model.add(k.layers.RepeatVector(num_output_dimensions))
    model.add(k.layers.LSTM(model_complexity,return_sequences=True))
    model.add(k.layers.Dense(model_complexity/2, activation=tf.sigmoid))
    model.add(k.layers.Dense(num_output_dimensions, activation=tf.sigmoid))


    return model


def run_lstm(train_X, train_Y, test_X, test_Y, model_complexity,batch_size):

    model = build_lstm(train_X[0].shape[0],train_X[0].shape[1],train_Y[0].shape[1],model_complexity)


    training_set = tf.data.Dataset.from_tensor_slices((    \
                            tf.cast(train_X, tf.float32), \
                            tf.cast(train_Y, tf.float32)))

    history = model.fit(train_X, train_Y, epochs=50,shuffle=True)
    #                    validation_data=(test_X, test_Y), verbose=2, shuffle=False)

    return model


def run_cross_validation(num_validations,samples,n_outputs,model_run):

    for i in range(num_validations):
        train_X, train_Y, test_X, test_Y  = reshuffle_observations(samples,0.80,n_outputs)
        print(train_X.shape, train_Y.shape, test_X.shape, test_Y.shape)
        model = model_run(train_X,train_Y,test_X,test_Y)
        return model


