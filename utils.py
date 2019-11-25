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


def get_percentage_diff(value_1, value_2):
    diff = np.abs(value_1 - value_2)
    sum_ = (value_1 + value_2) / 2.0
    diff = diff / sum_
    return diff


def get_item(df, itemcode, areacodes=None):
    condition = True
    if areacodes is not None:
        condition = df.areacode.isin(areacodes)
    item = df[(df.itemcode.isin(itemcode)) & condition].dropna(axis=1, how='all')
    return item    
    
def all_present_values_equal(dd1, dd2):
    are_equal = True
    missing = False
    for i in dd1.index:
        if i in dd2.index:
            are_equal = all(dd1.loc[i] == dd2.loc[i]) and are_equal
        else:
            missing = True
    if are_equal:
        print("All present items are equal")
    if missing:
        print("Some measurements exist in the first but not the second")
        

def get_ts_stats(df):
    grouped = df.groupby(['itemcode', 'areacode'])
    apply_func = lambda x: pd.Series({'years': x['year'].tolist(), 'cols': x.drop(columns=['areacode', 'itemcode', 'year']).dropna(axis=1, how='all').columns.tolist()})
    return grouped.apply(apply_func)


def get_element_label(elem):
    return f"{elem[0]} ({elem[1]})"

        
def get_column_unique_values(df, cols) -> pd.DataFrame:
    return df[cols].drop_duplicates()