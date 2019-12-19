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


def get_itemgroups_intersections(itemgroup_df):
    itemgroup_df = itemgroup_df.groupby(['itemgroupcode', 'itemgroup'])[['itemcode', 'item']].apply(
            lambda x: set(tuple(i) for i in x.values.tolist())).reset_index()
    itemgroup_df['key'] = 1
    
    merged = itemgroup_df.merge(itemgroup_df, how='outer', left_on='key', right_on='key')
    merged = merged[merged['itemgroupcode_x'] != merged['itemgroupcode_y']]
    merged['intersection'] = merged.apply(lambda x: x['0_x'].intersection(x['0_y']), axis=1)
    merged = merged[merged['intersection'].apply(len) > 0].drop(['0_x', '0_y'], axis=1)
    
    counted = set()
    for _, r in merged.iterrows():
        p1, p2 = (r['itemgroupcode_x'], r['itemgroupcode_y']), (r['itemgroupcode_y'], r['itemgroupcode_x'])
        if p1 not in counted and p2 not in counted:
            print(f"Intersection on {r['itemgroup_x']} ({r['itemgroupcode_x']}) and {r['itemgroup_y']} "
                  f"({r['itemgroupcode_y']}) on {r['intersection']}")
            counted.add((r['itemgroupcode_x'], r['itemgroupcode_y']))


def print_all_elements(df):
    if 'elementcode' in df.columns:
        tmp = df[['elementcode', 'element', 'unit']].drop_duplicates()
        print(tmp)
    else:
        print("No elementcode column")


def print_all_items(df):
    if 'itemcode' in df.columns:
        tmp = df[['itemcode', 'item']].drop_duplicates()
        print(tmp)
    else:
        print("No itemcode column")


def get_items_only_in_itemgroup(itemgroup_df, itemgroup_code):
    grouped = itemgroup_df.groupby('itemcode')['itemgroupcode'].apply(set)
    grouped = grouped[(grouped.apply(len) == 1) & (grouped.apply(lambda x: itemgroup_code in x))]
    return grouped.index.values


def get_items_in_one_group(itemgroup_df):
    grouped = itemgroup_df.groupby('itemcode')['itemgroupcode'].apply(set)
    return grouped[grouped.apply(len) == 1]


def get_countries_top_item(df, elementcode, year):
    data = df[(df.elementcode == elementcode) & (df.year == year)]
    top = data.groupby(['areacode', 'area', 'element', 'unit', 'elementcode']).apply(
        lambda x: x.sort_values('value', ascending=False)[['item', 'itemcode', 'value']].iloc[0])
    return top.reset_index()
