import os
from glob import glob
import pandas as pd
from utils import load_dataframe

def get_element_mapping(df):
    elements = df[['elementcode', 'element', 'unit']].drop_duplicates()
    elements['string'] = elements.apply(lambda x: f"{x['element']} ({x['unit']})", axis=1)
    return dict(elements[['elementcode', 'string']].values)

def get_all_element_mapping(data_dir):
    csv_files = glob(os.path.join(data_dir, "*.csv"))
    print(f"Fount {len(csv_files)} files in {data_dir}")
    
    mapping = []
    for file in csv_files:  # Iterate on all files
        df = load_dataframe(file)
        if 'elementcode' in df.columns:         
            df_mapping = get_element_mapping(df)
            mapping.append(df_mapping)
        else :
            print(f"Element Code not found in {file}")

    mapping = pd.DataFrame(data=[y  for x in mapping for y in x.items()], columns=['element_code', 'element_string'])
    mapping = mapping.drop_duplicates()
    assert mapping['element_code'].nunique() == len(mapping)
    return mapping

def get_item_mapping(df):
    items = df.groupby(['itemcode', 'item']).apply(lambda x: list(set(x['elementcode']))).reset_index().rename({0: 'elements'}, axis=1)
    return dict(items[['item', 'elements']].values)

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