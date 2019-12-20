import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import Adam
from tqdm import tqdm
import tensorflow as tf


def extract_timeseries_data(df, areacode, itemcode, elementcode, window, prediction_steps, scale_factor, year_max=2020):
    """ Extracts the time series data from the given df
    
    :param df: Dataframe in database format
    :param areacode: Areacode of interest
    :param window: Window for training
    :param prediction_steps: Predictions steps (typically 1)
    :param itemcode: Itemcode of interest
    :param elementcode: Elementcode
    :param scale_factor: Scale factor to divide
    :param year_max:
    :return:
    """
    # Select the given items
    data = df[(df.itemcode == itemcode) & (df.elementcode == elementcode) & (df.year < year_max) & (df.areacode == areacode)]
    area_codes = data.areacode.unique()
    
    values = []
    year_min, year_max = df.year.min(), df.year.max()
    start = year_min
    while start <= year_max - window - prediction_steps + 1:
        end = (start + window - 1) + prediction_steps
        for c in area_codes:
            area_data = data[(data.areacode == c)]
            vals = area_data[(area_data.year >= start) & (area_data.year <= end)]['value'].values
            if len(vals) != window + prediction_steps or np.isnan(vals).any():
                continue
            values.append(vals)
        start += 1
    
    values = np.vstack(values)
    x_values, y_values = values[:, :window] / scale_factor, values[:, window:] / scale_factor
    # print(f"Extracted {len(x_values)} windows for item {itemcode}, elementcode {elementcode}")
    return x_values, y_values


def get_model_error(model, x, y_true, n_features):
    X = x.reshape((x.shape[0], x.shape[1], n_features))
    predictions = model.predict(X)
    errors = (y_true - predictions) / y_true
    error = np.mean(errors.ravel())
    # print("Model got mean percentage error {:.2f}%".format(error * 100))
    return errors


def train_single_step_model(x_values, y_values, window, epochs=40, lr=0.01, verbose=0):
    n_features = 1
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(window, n_features)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer=Adam(lr=lr), loss='mse')
    
    Y = y_values
    X = x_values.reshape((x_values.shape[0], x_values.shape[1], n_features))
    model.fit(X, Y, epochs=epochs, verbose=verbose)
    
    errors = get_model_error(model, x_values, y_values, n_features)
    return model, errors


def predict_one_area(model, df, areacode, itemcode, elementcode, window, scale_factor, end_year, n_features=1):
    data = df[(df.itemcode == itemcode) & (df.elementcode == elementcode) & (df.areacode == areacode)]
    predictions = []
    tf.get_logger().setLevel('ERROR')
    
    year_max = df.year.max()
    start = year_max - window + 1
    end = year_max
    # Get the last window from data
    x = data[(data.year >= start) & (data.year <= end)]['value'].values / scale_factor
    if len(x) != window or np.isnan(x).any():
        print(f"Cannot predict on given window")
        return None
    
    predicted = model.predict(x.reshape(1, window, n_features))  # Predict the next year
    predictions.append((end + 1, predicted[0][0]))
    end += 1
    start += 1
    
    # Then start predicting in the future
    x = np.append(x, predicted)
    i = 1
    while start <= end_year - window:
        predicted = model.predict(x[i:].reshape(1, window, n_features))
        predictions.append((end + 1, predicted[0][0]))
        
        x = np.append(x, predicted)
        start += 1
        end += 1
        i += 1
    return np.vstack(predictions)


def train_models_on_all_items(df, areacode, window, step, scale_factor):
    models = {}
    item_elements = df[df.areacode == areacode][['itemcode', 'elementcode']].drop_duplicates().values
    for itemcode, elementcode in tqdm(item_elements):
        x_values, y_values = extract_timeseries_data(df, areacode=areacode, itemcode=itemcode, elementcode=elementcode,
                                                     window=window, prediction_steps=step, scale_factor=scale_factor)
        # print(f"Training model on item {itemcode} element {elementcode}")
        model = train_single_step_model(x_values, y_values, window)
        models[(itemcode, elementcode)] = model
    return models


def generate_predictions(df, areacode, window, step, scale_factor, end_year):
    tf.get_logger().setLevel('ERROR')
    
    data = df[df.areacode == areacode]
    
    prediction_dfs = []
    
    models = train_models_on_all_items(df, areacode=areacode, window=window, step=step, scale_factor=scale_factor)
    for k, v in models.items():
        itemcode, elementcode = k
        model, _ = v
        # Get last year of data
        year_start = data[(data.itemcode == itemcode) & (data.elementcode == elementcode)].year.max() + 1
        predictions = predict_one_area(model, data, areacode, itemcode, elementcode, window, scale_factor, end_year)
        
        item = data[(data.itemcode == itemcode)]['item'].values[0]
        element, unit = data[(data.elementcode == elementcode)][['element', 'unit']].values[0]
        area = data[data.areacode == areacode]['area'].values[0]
        rows = np.array([[itemcode, item, elementcode, element, unit, areacode, area, "P"]])  # Flag P for predicted
        rows = np.hstack([np.tile(rows, (end_year - year_start + 1, 1)), predictions])
        
        prediction_dfs.append(pd.DataFrame(data=rows,
                                           columns=["itemcode", "item", "elementcode", "element", "unit", "areacode", "area",
                                                    "flag", "year", "value"]))
    
    prediction_dfs = pd.concat(prediction_dfs, sort=False).reset_index(drop=True)
    prediction_dfs['value'] = prediction_dfs['value'].astype("float64") * scale_factor
    prediction_dfs['year'] = prediction_dfs['year'].apply(lambda x: int(float(x)))
    prediction_dfs['itemcode'] = prediction_dfs['itemcode'].astype("float64")
    prediction_dfs['elementcode'] = prediction_dfs['elementcode'].astype("float64")
    prediction_dfs['areacode'] = prediction_dfs['areacode'].astype('int64')
    return pd.concat([data, prediction_dfs], sort=False).reset_index(drop=True)
