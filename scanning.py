from typing import List, Tuple
import pandas as pd

from data_processing import load_dataframe
from utils import groupby_second_elem

def scan_columns(files: List[str], col_rename: dict = None, duplicate_cols=None) -> List[
    Tuple[List[str], List[str]]]:
    """ Scans the columns of a list of csv files, and returns (columns, [files])
    
    :param files: The list of files to scan
    :param mapping: The column renaming mapping
    :return: Returns a List of (columns, [files]), where all files with same columns are grouped
    """
    columns = []
    for f in files:
        df = load_dataframe(f, col_rename=col_rename, duplicate_cols=duplicate_cols)
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


def scan_column_duplicates(files: List[str], col_rename: dict = None):
    """ Scans for duplicate columns in each file of the given list
    
    :param files:
    :param mapping:
    :param check_columns:
    :return:
    """
    duplicates = []
    for f in files:
        df = load_dataframe(f, col_rename=col_rename)
        dups = get_duplicate_columns(df)
        if len(dups) > 0:
            duplicates.append((f, dups))
    
    grouped = groupby_second_elem(duplicates)
    return grouped