import pandas as pd
import numpy as np

def groupby_second_elem(l):
    grouped = []
    for f, d in l:
        found = False
        for d2, fs in grouped:
            if d == d2:
                fs.append(f)
                found = True
        if not found:
            grouped.append((d, [f]))
    return grouped


def is_unique_mapping(df, group_col, agg_col):
    grouped_1 = df.groupby(group_col)[agg_col].apply(lambda x: x.values.tolist())
    grouped_2 = df.groupby(agg_col)[group_col].apply(lambda x: x.values.tolist())
    return all(grouped_1.apply(len) == 1) and all(grouped_2.apply(len) == 1)


def get_percentage_diff(value_1, value_2):
    diff = np.abs(value_1 - value_2)
    sum_ = (value_1 + value_2) / 2.0
    diff = diff / sum_
    return diff


def get_item(df, itemcode, areacodes=None):
    condition = True
    if areacodes is not None:
        condition = df.areacode.isin(areacodes)
    item = df[(df.itemcode == itemcode) & condition].dropna(axis=1, how='all')
    return item    
    