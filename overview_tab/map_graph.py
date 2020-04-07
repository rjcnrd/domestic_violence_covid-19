import pandas as pd


def data_processing_for_graph(df, postal_code_df):
    """
    :param postal_code_df: data frame that includes the postal codes, the latitude and the longitude
    :param df: agression data
    :return: a dataframe with one row per postal code as index, with latitude, longitude and number of agressions
    """
    data = pd.DataFrame(df.groupby("postal_code")["first_time_exprience"].count())
    data = data.merge(postal_code_df, left_index=True, right_on="postcode", how="left")
    return data



