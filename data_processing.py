from typing import List, Tuple, Optional

import pandas as pd

from utils import groupby_second_elem


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


def load_dataframe(filename: str, mapping: dict = None, check_columns=None) -> pd.DataFrame:
    """ Loads a DataFrame, renames the column, and checks the given columns to see if it should drop them
    
    :param filename:
    :param mapping: Column renaming
    :param check_columns: Column names to drop if (1. All NaN, 2. Duplicate with other)
    :return:
    """
    df = pd.read_csv(filename, encoding="latin-1")
    df = rename_columns(df, mapping)
    
    if check_columns is not None:
        for c in check_columns:
            if c in df.columns and (col_is_duplicate(df, c) or df[c].isna().all()):  # If column is duplicate or NaN drop it
                df = df.drop(c, axis=1)
    
    if 'unit' in df.columns:
        df['unit'] = df['unit'].str.replace('gigagrams', 'Gigagrams')  # Hardcoded hack
    return df


def scan_columns(files: List[str], mapping: dict = None, check_columns: List[str] = None) -> List[
    Tuple[List[str], List[str]]]:
    """ Scans the columns of a list of csv files, and returns (columns, [files])
    
    :param files: The list of files to scan
    :param mapping: The column renaming mapping
    :param check_columns: Column names to drop if (1. All NaN, 2. Duplicate with other)
    :return: Returns a List of (columns, [files]), where all files with same columns are grouped
    """
    columns = []
    for f in files:
        df = load_dataframe(f, mapping=mapping, check_columns=check_columns)
        columns.append((f, set(df.columns.values)))
    
    column_sets = groupby_second_elem(columns)
    return column_sets


def get_duplicate_columns(df: pd.DataFrame):
    """ Scans all columns and returns those who are duplicates of each other
    
    :param df:
    :return:
    """
    cols = df.columns.values
    duplicates = []
    for i, c1 in enumerate(cols):
        for c2 in cols[i + 1:]:
            if all(df[c1] == df[c2]):
                duplicates.append((c1, c2))
    return duplicates


def scan_column_duplicates(files: List[str], mapping: dict = None, check_columns: List[str] = None):
    """ Scans for duplicate columns in each file of the given list
    
    :param files:
    :param mapping:
    :param check_columns:
    :return:
    """
    duplicates = []
    for f in files:
        df = load_dataframe(f, mapping=mapping, check_columns=check_columns)
        dups = get_duplicate_columns(df)
        if len(dups) > 0:
            duplicates.append((f, dups))
    
    grouped = groupby_second_elem(duplicates)
    return grouped


def get_column_unique_values(files: List[str], mapping: dict, check_columns, cols: List[str],
                             with_file=False) -> pd.DataFrame:
    """ Returns the unique values of the given columns (unique by row) accross all the given files
    
    :param files: List of files to scan
    :param mapping: Column rename mapping
    :param check_columns:
    :param cols:
    :param with_file: Add the filename column to the result
    :return:
    """
    all_vals = []
    for f in files:
        df = load_dataframe(f, mapping=mapping, check_columns=check_columns)  # Load df
        
        if all(c in df.columns for c in cols):  # Check all given cols are in it
            vals = df[cols].drop_duplicates()
            if with_file:
                vals['file'] = f
            all_vals.append(vals)
    if len(all_vals) == 0:
        return pd.DataFrame([])
    all_vals_df = pd.concat(all_vals)
    return all_vals_df.drop_duplicates()


def check_duplicate_items(df, items):
    for i in items:
        item_codes = df[df.item == i].itemcode.unique()
        if len(item_codes) > 1:
            if is_duplicate_item(df, i, item_codes):
                print(f"Duplicate item for {i} codes {item_codes}")


def get_duplicate_items(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """ Returns items that have two item codes within one dataframe
    
    :param df:
    :return:
    """
    if 'item' not in df.columns or 'itemcode' not in df.columns:
        return None
    item_to_code = df[['item', 'itemcode']].drop_duplicates().groupby('item')['itemcode'].agg(list)
    return item_to_code[item_to_code.apply(len) > 1]


def is_duplicate_item(df: pd.DataFrame, item_name: str, item_codes: List[str]) -> bool:
    """ Checks whether the given item with two item codes, has the same values for each duplicate
    
    :param df:
    :param item_name:
    :param item_codes:
    :return:
    """
    item_1 = df[(df.item == item_name) & (df.itemcode == item_codes[0])]
    item_2 = df[(df.item == item_name) & (df.itemcode == item_codes[1])]
    if item_1.shape[0] != item_2.shape[0]:
        return False
    return (item_1.drop('itemcode', axis=1).values == item_2.drop('itemcode', axis=1).values).all()


def load_clean_dataframe(filename, col_rename, duplicate_cols, check_columns) -> pd.DataFrame:
    """ Loads the dataframe with the given filename, renames columns, checks for duplicated items
    
    :param filename:
    :param col_rename:
    :param duplicate_cols:
    :param check_columns:
    :return:
    """
    df = load_dataframe(filename, col_rename, duplicate_cols)  # Load the DF
    
    if 'item' in df.columns and 'itemcode' in df.columns:  # Verify that it has item column
        duplicate_items = get_duplicate_items(df)  # Get all items that have two item codes
        if len(duplicate_items) > 0:
            for name, codes in duplicate_items.iteritems():
                if is_duplicate_item(df, name, codes):  # Check whether all the other columns but itemcode are equal
                    df = df.drop(df[df.itemcode == codes[1]].index)  # Drop duplicates if exactly same value
                    print(f"Dropped duplicate item {name} with codes {codes} (Dropped {codes[1]})")
    
    return df.drop(columns=check_columns, errors='ignore')
