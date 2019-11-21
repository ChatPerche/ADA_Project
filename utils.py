import pandas as pd
import os
from tqdm import tqdm
from glob import glob
from mappings import get_all_element_mapping, get_all_item_mapping, rename_columns


def load_dataframe(filename):
    df = pd.read_csv(filename, encoding="latin-1")
    return rename_columns(df)

def get_element_from_mapping(elementcode, element_mapping, key='elementcode'):
    fltr = element_mapping[element_mapping[key] == elementcode]
    if len(fltr) == 0:
        return ""
    elem = fltr.iloc[0]
    return f"{elem.element} ({elem.unit})"


def reshape_dataframe(df, element_mapping):
    df = df.drop(['yearcode', 'unit', 'element', 'flag', 'areacode', 'itemcode'], axis=1)  # Drop unused columns
    df = df.set_index(['area', 'elementcode', 'item', 'year'])
    df = df['value'].unstack(1)
    df.columns = [get_element_from_mapping(x, element_mapping) for x in df.columns]
    df = df.reset_index()
    return df


def percentage_of_total(df, total_item, column):
    df_total = df[df.item == total_item]
    percentage = df.apply(lambda r: (r[column] / df_total[(df_total.year == r.year)][column].iloc[0]) * 100, axis=1)
    new_col_name = f"{column} %"
    df.loc[:, new_col_name] = percentage
    return df

def element_to_item_mapping(data_path,element_mapping,item_mapping,
                             build_element_df = False, output_path = None):

    assert((build_element_df is False) or (output_path is not None))

    csv_files       = glob(os.path.join(data_path, "*/*.csv"))
    dataframes          = {}
    element_to_items    = {}

    # Create one dataframe per element and append corresponding rows from each csv
    tqdm_progress_1 = tqdm(csv_files)
    tqdm_progress_1.set_description("Breaking up Data by Element")
    for file in tqdm_progress_1:
        df = load_dataframe(file)
        if 'itemcode' in df.columns:
            for elem_code, _ in element_mapping.items():
                df_slice = df[df.elementcode == elem_code].copy()
                if len(df_slice) is not 0:
                    for item_code in df_slice.itemcode.unique():
                        if elem_code not in element_to_items:
                            element_to_items[elem_code] = [item_code]
                        elif item_code not in element_to_items[elem_code]:
                            element_to_items[elem_code].append(item_code)
                    if elem_code not in dataframes:
                        dataframes[elem_code] = df_slice
                    else:
                        dataframes[elem_code] = dataframes[elem_code].append(df_slice,sort=False)

    if build_element_df:
        for elem_code, df in dataframes.items():
            filename = element_mapping[elem_code][0]+'_'+element_mapping[elem_code][1]+'.pickle'
            filename = filename.replace('/','_').replace(' ','_')
            path     = os.path.join(output_path,filename)
            df.to_pickle(path)

    return element_to_items

def load_element_dataframes(data_path,element_mapping):
    dataframes = {}
    for elem_code, _ in element_mapping.items():
        filename = element_mapping[elem_code][0] + '_' + element_mapping[elem_code][1] + '.pickle'
        filename = filename.replace('/', '_').replace(' ', '_')
        path = os.path.join(data_path, filename)
        if os.path.exists(path):
            dataframes[elem_code] = pd.read_pickle(path)
    return dataframes

import ipywidgets as widgets

def explore_items(dataframes,element_mapping,item_mapping,elem_to_item):
    item_select = widgets.Dropdown(
        options=[(element_name[0], element_code) for element_code, element_name in
                 element_mapping.items()],
        value=list(element_mapping.values())[0][0],
        description='Select Item:',
        disabled=False,
    )
    selector=widgets.GridBox([item_select], layout=widgets.Layout(grid_template_columns="repeat(1, 300px)"))
    return selector


#  tqdm_progress_2 = tqdm()
  #œ  tqdm_progress_2.set_description("Running Joins on 'Country','Area'")
'''
    for elem_code, dataframe in dataframes.items():
        df = dataframe.drop(['year', 'unit', 'element','elementcode', 'flag', 'area', 'item'], axis=1)
        df = df.set_index(['areacode', 'yearcode'])
        reshaped_dataframe = None

        tqdm_progress_3 = tqdm(element_to_items[elem_code])
        tqdm_progress_3.set_description("Running Join for "+str(element_mapping[elem_code]))

        for item_code in tqdm_progress_3:
            new_column_name = item_mapping[item_code] + ' ( ' + str(item_code) + ' )'
            column_df = pd.DataFrame(df[df.itemcode==item_code]['value'])
            column_df = column_df.rename(columns={'value':new_column_name})
            if reshaped_dataframe is None:
                reshaped_dataframe = column_df
            else:
                reshaped_dataframe[new_column_name] = column_df[new_column_name]

        reshaped_dataframe.to_csv(path)
'''
