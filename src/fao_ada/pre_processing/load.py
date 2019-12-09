import os
from typing import Optional

import pandas as pd

from fao_ada.utils import col_is_duplicate, is_unique_mapping

COL_RENAME = {'country': 'area', 'countrycode': 'areacode'}
DUPLICATE_COLS = ["elementgroup", "yearcode"]

ITEM_MAPPING = ['itemcode', 'item']
ELEMENT_MAPPING = ['elementcode', 'element', 'unit']


def read_original_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, encoding="latin-1")
    df.columns = [x.lower().replace(" ", "") for x in df.columns]  # Remove spaces and lowercase
    df = df.rename(columns=COL_RENAME)
    return df


def drop_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ Scans the DF and checks if the columns in `DUPLCIATE_COLS` are duplicates, if yes it drops them.
    
    :param df:
    :return:
    """
    for c in DUPLICATE_COLS:
        if c in df.columns and col_is_duplicate(df, c):
            df = df.drop(c, axis=1)
    return df


def load_dataframe(filename: str) -> pd.DataFrame:
    df = read_original_csv(filename)
    df = drop_duplicate_columns(df)
    
    if 'unit' in df.columns:
        df['unit'] = df['unit'].str.replace('gigagrams', 'Gigagrams')  # Hardcoded hack
    return df


def drop_all_itemgroups(df: pd.DataFrame, item_groups: pd.DataFrame) -> pd.DataFrame:
    itemgroup_codes = item_groups['itemgroupcode'].unique()
    itemcodes = item_groups['itemcode'].unique()
    df = df[(~df['itemcode'].isin(itemgroup_codes)) & (df['itemcode'].isin(itemcodes))]  # Drop all item groups
    return df


def drop_all_country_groups(df: pd.DataFrame, country_groups: pd.DataFrame) -> pd.DataFrame:
    countrygroup_codes = country_groups['countrygroupcode'].unique()
    df = df[~df['areacode'].isin(countrygroup_codes)]
    return df


def load_and_clean_df(csv_file: str, country_groups: Optional[str] = None,
                      item_groups: Optional[str] = None) -> pd.DataFrame:
    """
    This function loads the csv file, renames the columns (remove spaces and all in lowercase), and :
    - Drops all country groups if `country_groups` is not None
    - Drops all item groups if `item_groups` is not None (and also only keeps itemcodes that are in an itemgroup)
    - Checks if the mappings (item <=> itemcode) and (elementcode <=> (element, unit)) is unique
    
    :param csv_file:
    :param country_groups:
    :param item_groups:
    :return:
    """
    basename = os.path.basename(csv_file)
    df = load_dataframe(csv_file)
    
    if country_groups is not None:  # Drop country groups if specified
        country_df = load_dataframe(country_groups)
        df = drop_all_country_groups(df, country_df)
    
    if item_groups is not None:
        item_group_df = load_dataframe(item_groups)
        df = drop_all_itemgroups(df, item_group_df)
    
    if 'itemcode' in df.columns:
        unique_item = is_unique_mapping(df, 'itemcode', 'item')
        if not unique_item:
            print(f"File {basename} doesn't have a unique itemcode <=> item mapping")
    
    if 'elementcode' in df.columns:
        unique_element = is_unique_mapping(df, 'elementcode', ['element', 'unit'])
        if not unique_element:
            print(f"File {basename} doesn't have a unique elementcode <=> (element, unit)")
    return df.drop(columns=['flag'])
