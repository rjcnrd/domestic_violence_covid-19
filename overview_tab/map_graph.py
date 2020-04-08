import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

FAMILY = "PT Sans"


def data_processing_for_graph(df, postal_code_df, map_threshold):
    """
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :param postal_code_df: data frame that includes the postal codes, the latitude and the longitude
    :param df: survey data
    :return: a dataframe with one row per postal code as index, with latitude, longitude and number of incidents
    """
    data = pd.DataFrame(df.groupby("postal_code")["first_time_exprience"].count())
    data = data.rename(columns={"first_time_exprience": "count_incidents"})
    data = data[data.count_incidents > map_threshold]
    data = data.merge(postal_code_df, left_index=True, right_on="postcode", how="left")
    return data


def map_graph(df, postal_code_df, map_threshold):
    """
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :param df: dummy data
    :param postal_code_df: postal code data frame
    :return: map of UK with the number of agressions
    """
    data = data_processing_for_graph(df, postal_code_df, map_threshold)
    fig = px.scatter_mapbox(data,
                            lat="latitude",
                            lon="longitude",
                            size="count_incidents",  # size of the dots
                            color_discrete_sequence=['#d80052'],  # dots are pink
                            zoom=4.2,  # add a zoom of size of great britain
                            width=600,  # width of the graph
                            height=630,  # height of the graph
                            hover_name="count_incidents")

    fig.update_layout(mapbox_style="carto-positron",  # Chooses the type of map in the background
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      title=dict(text="Number of incidents reported per postal code",
                                 x=0.5,
                                 font=dict(family=FAMILY,
                                           color="white",
                                           size=24)),
                      mapbox=dict(center=go.layout.mapbox.Center(lat=54.237933, lon=-2.36967)))

    return fig