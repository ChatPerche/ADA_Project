import os
from glob import glob
import pandas as pd
from data_processing import get_column_unique_values, load_dataframe

def get_mapping(csv_files, col_rename, check_cols, columns):
    unique_vals = get_column_unique_values(csv_files, col_rename, check_cols, columns).values
    if len(columns) == 3:
        unique_vals = [(x[0], (x[1], x[2])) for x in unique_vals]
    return dict(unique_vals)

def get_area_mapping(csv):
    df = load_dataframe(csv)
    areas = df[['countrycode', 'country']].drop_duplicates()
    return dict(areas.values)

def get_country_groups(csv):
    df = load_dataframe(csv)
    grouped = df.groupby('countrygroupcode')['countrycode'].agg(set).reset_index()
    return dict(grouped.values)