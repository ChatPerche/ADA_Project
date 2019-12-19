import numpy as np
import pandas as pd


def get_correlation(values):
    values = values[['value_x', 'value_y']].values
    return np.corrcoef(values[:, 0], values[:, 1])[0][1]


def compute_emission_correlations(emissions_df, other_dfs):
    """ Computes the correlations between each item of `emissions_df` to each item in `other_dfs`
    
    First merges on [`areacode`, `area`, `year`]
    Then groups per area and item and computes the correlations over the years
    Finally it groups over all areas and returns the mean correlation over all areas
    
    :param emissions_df:
    :param other_dfs:
    :return:
    """
    group_cols = ['areacode', 'area', 'itemcode_x', 'item_x', 'elementcode_x', 'element_x', 'unit_x', 'itemcode_y', 'item_y',
                  'elementcode_y', 'element_y', 'unit_y']
    
    group_cols_2 = ['itemcode_x', 'item_x', 'elementcode_x', 'element_x', 'unit_x', 'itemcode_y', 'item_y', 'elementcode_y',
                    'element_y', 'unit_y']
    final_dfs = []
    for df in other_dfs:
        merged = emissions_df.merge(df, on=['areacode', 'area', 'year'], how='outer')
        merged = merged.groupby(group_cols).apply(lambda x: get_correlation(x)).reset_index().rename(
                columns={0: "correlation"})
        merged = merged.groupby(group_cols_2)['correlation'].mean().reset_index()
        final_dfs.append(merged)
    
    return pd.concat(final_dfs).dropna()


def compute_emissions_ratios(dictionary):
    dfs = []
    for f, v in dictionary.items():
        df = pd.read_csv(f)
        df = df[(df.elementcode == v) & (df.year < 2020)]
        df = df.groupby(['itemcode', 'item', 'elementcode', 'element', 'year', 'unit'])['value'].sum().reset_index()
        total_emissions = df.groupby(['elementcode', 'element', 'unit', 'year'])['value'].sum().reset_index()
        merged = df.merge(total_emissions, on=['elementcode', 'element', 'unit', 'year'])
        merged['ratio'] = (merged['value_x'] / merged['value_y'])
        merged = merged.drop(columns=['value_x', 'value_y'])
        final = merged.groupby(['itemcode', 'item', 'elementcode', 'element', 'unit'])['ratio'].mean().reset_index()
        #final['ratio'] = final['ratio'].apply(lambda x: "{:.2f}%".format(x*100))
        dfs.append(final)
    
    df = pd.concat(dfs).drop(columns=['elementcode', 'unit']).pivot(index='item', columns='element', values='ratio').fillna(
            0)
    
    return df


def compute_emission_factor(dictionary):
    dfs = []
    for f, v in dictionary.items():
        # Production/emission element codes
        prod, em = v
        df = pd.read_csv(f)
        element = df[df.elementcode == em]['element'].values[0]
        new_unit = f"{df[df.elementcode == em]['unit'].values[0]} / {df[df.elementcode == prod]['unit'].values[0]}"
        df = df[df.elementcode.isin([prod, em]) & (df.year < 2020)]
        df = df.drop(['element', 'unit'], axis=1).set_index(
                ['areacode', 'area', 'itemcode', 'year', 'item', 'elementcode']).unstack(-1).reset_index()
        df.columns = [x[0] if type(x[1]) == str else x[1] for x in df.columns]
        df["value"] = df[em] / df[prod]
        df["unit"] = new_unit
        df["origin"] = element
        df = df.drop([prod, em], axis=1)
        dfs.append(df)
    df = pd.concat(dfs, sort=False).dropna()
    df = df.groupby(['areacode', 'area', 'itemcode', 'year', 'item', 'unit'])['value'].sum().reset_index()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna().groupby(['year', 'item', 'unit', 'itemcode'])['value'].mean().reset_index()
    return df
