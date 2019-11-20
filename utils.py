import pandas as pd

def groupby_second_elem(l):
    grouped = []
    for f, d in l:
        found = False
        for d2, fs in grouped:
            if d == d2:
                fs.append(f)
                found=True
        if not found:
            grouped.append((d, [f]))
    return grouped




def is_unique_mapping(df, group_col, agg_col):
    grouped_1 = df.groupby(group_col)[agg_col].apply(lambda x: x.values.tolist())
    grouped_2 = df.groupby(agg_col)[group_col].apply(lambda x: x.values.tolist())
    return all(grouped_1.apply(len) == 1) and all(grouped_2.apply(len) == 1)


def get_element_from_mapping(elementcode, element_mapping, key='elementcode'):
    fltr = element_mapping[element_mapping[key] == elementcode]
    if len(fltr) == 0:
        return ""
    elem = fltr.iloc[0]
    return f"{elem.element} ({elem.unit})"


def reshape_dataframe(df):
    df = df.drop(['yearcode', 'unit', 'element', 'flag', 'areacode', 'itemcode'], axis=1)  # Drop unused columns
    df = df.set_index(['area', 'elementcode', 'item', 'year'])
    df = df['value'].unstack(1)
    df = df.reset_index()
    del df.columns.name
    return df


def percentage_of_total(df, total_item, column):
    df_total = df[df.item == total_item]
    percentage = df.apply(lambda r: (r[column] / df_total[(df_total.year == r.year)][column].iloc[0]) * 100, axis=1)
    new_col_name = f"{column} %"
    df.loc[:, new_col_name] = percentage
    return df