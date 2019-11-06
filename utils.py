import pandas as pd

def rename_columns(df):
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "")
    return df

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