def split_legislative(df):
    """Splits the dataframe by legislative."""
    dfs = [df.loc[df["Legislative"] == i] for i in range(3)]
    return dfs
