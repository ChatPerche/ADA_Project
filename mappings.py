import os
from glob import glob
import pandas as pd
from utils import rename_columns

def get_element_mapping(df):
    elements = df[['elementcode', 'element', 'unit']].drop_duplicates()
    return elements

def get_all_element_mapping(data_dir):
    csv_files = glob(os.path.join(data_dir, "*.csv"))
    print(f"Fount {len(csv_files)} files in {data_dir}")
    
    mapping = []
    for file in csv_files:  # Iterate on all files
        df = rename_columns(pd.read_csv(file, encoding="latin-1"))
        if 'elementcode' in df.columns:         
            df_mapping = get_element_mapping(df)
            mapping.append(df_mapping)
        else :
            print(f"Element Code not found in {file}")
            
    mapping = pd.concat(mapping)
    mapping = mapping.assign(unit=mapping['unit'].str.replace("Gigagrams", "gigagrams")) #Data cleaning
    mapping = mapping.drop_duplicates()
    assert mapping['elementcode'].nunique() == len(mapping)
    
    mapping = {m['elementcode']: (m['element'], m['unit']) for _, m in mapping.iterrows()}
    return mapping

def get_item_mapping(df):
    items = df[['itemcode', 'item']].drop_duplicates()
    return items

def get_all_item_mapping(data_dir):
    csv_files = glob(os.path.join(data_dir, "*.csv"))
    print(f"Fount {len(csv_files)} files in {data_dir}")
    
    mapping = []
    for file in csv_files:  # Iterate on all files
        df = rename_columns(pd.read_csv(file, encoding="latin-1"))
        if 'itemcode' in df.columns:         
            df_mapping = get_item_mapping(df)
            mapping.append(df_mapping)
        else :
            print(f"Item Code not found in {file}")
            
    mapping = pd.concat(mapping)
    mapping = mapping.drop_duplicates()
    assert mapping['itemcode'].nunique() == len(mapping)
    mapping = {m['itemcode']: m['item'] for _, m in mapping.iterrows()}
    return mapping

def get_area_mapping(df):
    areas = df[['areacode', 'area']].drop_duplicates()
    return areas