import numpy as np
import pandas as pd


def get_correlation(values):
    values = values[['value_x', 'value_y']].values
    return np.corrcoef(values[:, 0], values[:, 1])[0][1]


def compute_emission_correlations(emissions_df, other_dfs):
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
    
    return pd.concat(final_dfs)


def compute_emissions_ratios(dictionnary):
    dfs = []
    for f, v in dictionnary.items():
        df = pd.read_csv(f)
        df = df[(df.elementcode == v) & (df.year < 2020)]
        df = df.groupby(['itemcode', 'item', 'elementcode', 'element', 'year', 'unit'])['value'].sum().reset_index()
        total_emissions = df.groupby(['elementcode', 'element', 'unit', 'year'])['value'].sum().reset_index()
        merged = df.merge(total_emissions, on=['elementcode', 'element', 'unit', 'year'])
        merged['ratio'] = merged['value_x'] / merged['value_y']
        merged = merged.drop(columns=['value_x', 'value_y'])
        final = merged.groupby(['itemcode', 'item', 'elementcode', 'element', 'unit'])['ratio'].mean().reset_index()
        dfs.append(final)
    
    df = pd.concat(dfs).drop(columns=['elementcode', 'unit']).pivot(index='item', columns='element', values='ratio').fillna(
        0)
    return df
