import pandas as pd
import geopandas as gpd


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


def is_unique_mapping(df, group_col, agg_col):
    grouped_1 = df.groupby(group_col)[agg_col].apply(lambda x: set(tuple(i) for i in x.values))
    grouped_2 = df.groupby(agg_col)[group_col].apply(lambda x: set(i for i in x.values))
    return all(grouped_1.apply(len) == 1) and all(grouped_2.apply(len) == 1)


def check_mapping_multiple_files(csv_files, group_col, agg_col):
    dfs = []
    for f in csv_files:
        tmp = pd.read_csv(f)
        if group_col[0] in tmp.columns:
            tmp = tmp[group_col + agg_col].drop_duplicates()
            dfs.append(tmp)
        else:
            print(f"Could not find column {group_col[0]} in {f}")
    df = pd.concat(dfs).reset_index(drop=True).drop_duplicates()
    return is_unique_mapping(df, group_col[0], agg_col)


def merge_with_geopandas(df, shapefile):
    world_map = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    world_map.columns = ['area', 'iso3code', 'geometry']
    plot_map = world_map.merge(df.drop('area', axis=1), on='iso3code', how='inner')
    return plot_map


def normalize_by_population(df, population_df):
    population_df = population_df[population_df.elementcode == 511][['areacode', 'year', 'value']].rename(
            columns={'value': 'population'})
    population_df['population'] *= 1000  # Rectify unit
    df = df.merge(population_df, left_on=['areacode', 'year'], right_on=['areacode', 'year'], how='left')
    df['value'] = df['value'] / df['population']
    return df.drop(columns='population')
