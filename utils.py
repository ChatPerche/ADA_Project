
def rename_columns(df):
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "")
    return df