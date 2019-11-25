from typing import List, Tuple, Optional

import pandas as pd

from utils import groupby_second_elem, get_column_unique_values


def rename_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """ Function that renames the columns of a given dataframe by putting all in lowercase and removing spaces
    If mapping != None, it should be a dict with column mapping to rename
    
    :param df : Dataframe
    :param mapping: Dictionary for column rename
    :return:
    """
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "")
    if mapping is not None:
        df = df.rename(columns=mapping)
    return df


def col_is_duplicate(df: pd.DataFrame, col: str) -> bool:
    """ Checks whether the given column is equal to any other in the given dataframe
    
    :param df: The dataframe
    :param col: The column to check
    :return:
    """
    columns = df.columns
    for c in columns:
        if c != col:
            is_equal = (df[col] == df[c]).all()
            if is_equal:
                return True
    return False


def load_dataframe(filename: str, col_rename: dict=None, duplicate_cols=None):
    df = pd.read_csv(filename, encoding="latin-1")
    df = rename_columns(df, col_rename)
    
    if duplicate_cols != None:
        for c in duplicate_cols:
            if c in df.columns and col_is_duplicate(df, c):
                df = df.drop(c, axis=1)
    if 'unit' in df.columns:
        df['unit'] = df['unit'].str.replace('gigagrams', 'Gigagrams')  # Hardcoded hack
    return df

def get_duplicate_items(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """ Returns items that have two item codes within one dataframe
    
    :param df:
    :return:
    """
    if 'item' not in df.columns or 'itemcode' not in df.columns:
        return None
    item_to_code = df[['item', 'itemcode']].drop_duplicates().groupby('item')['itemcode'].agg(list)
    duplicated = item_to_code[item_to_code.apply(len) > 1].reset_index()
    
    duplicated_indices = []
    for i, r in duplicated.iterrows():
        item_1 = df[(df.item == r['item']) & (df.itemcode == r['itemcode'][0])].drop('itemcode', axis=1)
        item_2 = df[(df.item == r['item']) & (df.itemcode == r['itemcode'][1])].drop('itemcode', axis=1)
        
        if (item_1.shape[0] == item_2.shape[0]) and (item_1.values == item_2.values).all():
            duplicated_indices.append(i)
    return duplicated.loc[duplicated_indices]


def load_clean_dataframe(filename: str, col_rename: dict = None, duplicate_cols=None) -> pd.DataFrame:
    df = load_dataframe(filename, col_rename, duplicate_cols=duplicate_cols)
    df = df.dropna(how='all', axis=1) # Drop NaN columns
    
        
    duplicated_items = get_duplicate_items(df)
    if duplicated_items is not None and len(duplicated_items) > 0:
        for i, r in duplicated_items.iterrows():
            df = df.drop(df[df.itemcode == r['itemcode'][1]].index)  # Drop duplicates if exactly same value
            print(f"Dropped {r['item']} with code {r['itemcode'][1]}")
    return df


def get_all_column_unique_values(files, rename_cols, duplicate_cols, cols, with_file=False):
    dfs = []
    for f in files:
        df = load_dataframe(f, rename_cols, duplicate_cols)
        if all(c in df.columns for c in cols):
            df = get_column_unique_values(df, cols)
            if with_file:
                df["file"] = f
            dfs.append(df)
    return pd.concat(dfs).drop_duplicates()
            
                       
def load_all_df_with_schema(files, schema, column_rename, check_columns, drop_columns):
    dfs = []
    for f in files:
        df = load_clean_dataframe(f, column_rename, check_columns, drop_columns) # Load the DF
        if all(x in schema for x in df.columns):  # Check if schema corresponds
            df = df.assign(file=f)
            dfs.append(df)
    df = pd.concat(dfs).reset_index(drop=True)
    shape = df.shape[0]
    
    to_keep = df.drop(columns=['file']).drop_duplicates().index # Drop all duplicated row, after removing `file`
    df = df.loc[to_keep].reset_index(drop=True)
    print(f"Dropped {shape - df.shape[0]} duplicate rows")
    return df

def load_item_groups(files):
    dfs = []
    for f in files:
        df = load_dataframe(f)
        dfs.append(df)
    df = pd.concat(dfs).reset_index(drop=True)    
    return df