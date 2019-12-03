def split_legislative(df, reset_index=True):
    """Splits the dataframe by legislative."""
    dfs = [df.loc[df["Legislative"] == i] for i in range(3)]
    if reset_index:
        dfs = [df.reset_index(drop=True) for df in dfs]
    return dfs
