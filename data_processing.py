import pandas as pd
import numpy as np
from utils import groupby_second_elem

def rename_columns(df, mapping):
    # This function renames all columns: sets them to lowercase and removes spaces
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "")
    if mapping is not None:
        df = df.rename(columns=mapping)
    return df

def col_is_duplicate(df, col):
    columns = df.columns
    for c in columns:
        if c != col:
            is_equal = all(df[col] == df[c])
            if is_equal:
                return True
    return False


def load_dataframe(filename, mapping=None, drop=None):
    # Loads dataframe and renames columns
    df = pd.read_csv(filename, encoding="latin-1")
    df = rename_columns(df, mapping)
    
    if drop is not None:
        for c in drop:  # Iterate on columns to drop
            if c in df.columns and (col_is_duplicate(df, c) or df[c].isna().all()):
                df = df.drop(c, axis=1)
    if 'unit' in df.columns:
        df['unit'] = df['unit'].str.replace('gigagrams', 'Gigagrams') # Hardcoded hack
    return df

def scan_columns(files, mapping=None, drop=None):
    # Scans the columns and returns a list of (columns, files)
    columns = []
    for f in files:
        df = load_dataframe(f, mapping=mapping, drop=drop)
        columns.append((f, set(df.columns.values)))
    
    column_sets = groupby_second_elem(columns)
    return column_sets


def get_duplicate_columns(df):
    # Returns the pairs of duplicate columns in the dataframe
    cols = df.columns.values
    duplicates = []
    for i, c1 in enumerate(cols):
        for c2 in cols[i+1:]:
            if all(df[c1] == df[c2]):
                duplicates.append((c1, c2))
    return duplicates

def scan_column_duplicates(files, mapping=None, drop=None):
    duplicates = []
    for f in files:
        df = load_dataframe(f, mapping=mapping, drop=drop)
        dups = get_duplicate_columns(df)
        if len(dups) > 0:
            duplicates.append((f, dups))
            
    grouped = groupby_second_elem(duplicates)
    return grouped

def get_column_unique_values(files, mapping, drop, cols, with_file=False):
    all_vals = []
    for f in files:
        df = load_dataframe(f, mapping=mapping, drop=drop)
        if all(c in df.columns for c in cols):
            vals = df[cols].drop_duplicates()
            if with_file:
                vals['file'] = f
            all_vals.append(vals)
    all_vals_df = pd.concat(all_vals)
    return all_vals_df.drop_duplicates()

def check_duplicate_items(df, items):
    duplicated = []
    for i in items:
        item_codes = df[df.item == i].itemcode.unique()
        if len(item_codes) > 1:
            if (df[df.itemcode == item_codes[0]].drop('itemcode', axis=1).values == df[df.itemcode == item_codes[1]].drop('itemcode', axis=1).values).all():
                print(f"Duplicate item for {i} codes {item_codes}")

def get_duplicate_items(df):
    if 'item' not in df.columns or 'itemcode' not in df.columns:
        return None
    item_to_code = df[['item', 'itemcode']].drop_duplicates().groupby('item')['itemcode'].agg(set)
    return item_to_code[item_to_code.apply(len) > 1]

def load_clean_dataframe(filename, col_rename, duplicate_cols, drop_cols):
    df = load_dataframe(filename, col_rename, duplicate_cols)
    if 'item' in df.columns and 'itemcode' in df.columns:
        item_to_code = df[['item', 'itemcode']].drop_duplicates().groupby('item')['itemcode'].count()
        if any(item_to_code > 1):
            print(filename)
    return df