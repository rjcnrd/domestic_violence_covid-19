import pandas as pd
import plotly.graph_objects as go
import numpy as np
import warnings

warnings.filterwarnings("ignore", 'This pattern has match groups')
pd.options.mode.chained_assignment = None  # default='warn'

FAMILY = "PT Sans"
token = "pk.eyJ1IjoiYW1lbWV1cmVyIiwiYSI6ImNrOHBxdHFmMTBqN2MzZ25sY3c1eHk4ZmoifQ.He4E-itQVmRV4znQMhXTjw"
style_url = "mapbox://styles/amemeurer/ck8rg6v0k164o1inv1mttdq10"


def postal_code_treatment(survey_data, postal_code_col="postal_code"):
    # Deletes the spacing at the beginning
    survey_data[postal_code_col] = survey_data[postal_code_col].str.lstrip()
    survey_data[postal_code_col] = survey_data[postal_code_col].str.upper()

    # Start with a letter and Contains a number
    data_to_display = survey_data.loc[survey_data[postal_code_col].str.contains('(^[A-Z])(.*\d+)')]
    data_to_display["area"] = data_to_display[postal_code_col].str.extract('^(\D*)')
    data_to_display["area"] = data_to_display["area"].str.rstrip()
    return data_to_display


def apply_threshold_merge_postcode(survey_df, column, postal_code_df, map_threshold):
    """
    :param survey_df: survey data. Using the postal code
    :param column: the column on which to do the filtering
    :param postal_code_df: data frame that includes the postal codes, the latitude and the longitude
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :return: a data frame with a filter on the threshold and a merge with postal code
    """
    df = survey_df[survey_df[column] > map_threshold]
    df = df.merge(postal_code_df, left_index=True, right_on="area", how="left")
    return df


def data_processing_for_graph(survey_df, postal_code_df, map_threshold):
    """
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :param postal_code_df: data frame that includes the postal codes, the latitude and the longitude
    :param data: survey_df data. Using the postal code and the "first time experience" but only for the groupby, could be another columns
    :return: a dataframe with one row per postal code as index, with latitude, longitude and number of incidents
    """
    data = postal_code_treatment(survey_df)
    safety_df = pd.DataFrame(data.loc[data.safety < 3].groupby("area")["safety"].count())
    safety_df = apply_threshold_merge_postcode(safety_df, "safety", postal_code_df, map_threshold)

    safety_change_df = pd.DataFrame(data.loc[data.safety_change == "Worse"].groupby("area")["safety_change"].count())
    safety_change_df = apply_threshold_merge_postcode(safety_change_df, "safety_change", postal_code_df, map_threshold)

    mental_health_df = pd.DataFrame(data.loc[data.mental_health < 3].groupby("area")["mental_health"].count())
    mental_health_df = apply_threshold_merge_postcode(mental_health_df, "mental_health", postal_code_df, map_threshold)

    working_situation_df = pd.DataFrame(
        data.loc[data.working_situation.isin(["No, I have been furloughed because of the lockdown",
                                              "No, I have been made redundant because of the lockdown",
                                              "No, I have had to stop working for other reasons related to COVID-19"])].groupby(
            "area")["working_situation"].count())
    working_situation_df = apply_threshold_merge_postcode(working_situation_df, "working_situation", postal_code_df,
                                                          map_threshold)

    all_reports_df = pd.DataFrame(data.groupby("area")["safety"].count())
    all_reports_df = all_reports_df.rename(columns={"safety": "all_reports"})
    all_reports_df = apply_threshold_merge_postcode(all_reports_df, "all_reports", postal_code_df, map_threshold)
    all_reports_df = all_reports_df.merge(safety_df[["safety", "area"]], left_on="area", right_on="area", how="left")
    all_reports_df = all_reports_df.merge(safety_change_df[["safety_change", "area"]], left_on="area", right_on="area",
                                          how="left")
    all_reports_df = all_reports_df.merge(mental_health_df[["mental_health", "area"]], left_on="area", right_on="area",
                                          how="left")
    all_reports_df = all_reports_df.merge(working_situation_df[["working_situation", "area"]], left_on="area",
                                          right_on="area", how="left")
    all_reports_df[["safety", "safety_change", "mental_health", "working_situation"]] = all_reports_df[
        ["safety", "safety_change", "mental_health", "working_situation"]].fillna("[Too low to be displayed]")
    return all_reports_df, safety_df, safety_change_df, mental_health_df, working_situation_df


def map_graph(survey_df, postal_code_df, map_threshold, bubble_size=2):
    """
    :param bubble_size: size of the reference bubble in the map. The bigger the bubble_size, the smaller the bubble
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :param survey_df: dummy data
    :param postal_code_df: postal code data frame
    :return: map of UK with the number of agressions
    """
    all_reports_df, safety_df, safety_change_df, mental_health_df, working_situation_df = data_processing_for_graph(
        survey_df, postal_code_df, map_threshold)

    # All reports
    fig = go.Figure(
        data=go.Scattermapbox(
            lat=all_reports_df.latitude,
            lon=all_reports_df.longitude,
            mode='markers',
            hovertemplate="<b>We have %{marker.size:,} reports from %{text} during the lockdown</b><br>" +
                          "<br><i>%{customdata[0]}</i> report to feel unsafe" +
                          "<br><i>%{customdata[1]}</i> report to feel less safe" +
                          "<br><i>%{customdata[2]}</i> report to have a low mental health" +
                          "<br><i>%{customdata[3]}</i> report that they had to stop working" +
                          "<extra></extra>",
            text=all_reports_df.area_name,
            customdata=np.stack((all_reports_df['safety'], all_reports_df['safety_change'],
                                 all_reports_df['mental_health'], all_reports_df['working_situation']), axis=-1),
            marker=go.scattermapbox.Marker(
                sizeref=bubble_size,
                size=all_reports_df.all_reports,
                sizemode ="area",
                # size of the dots
                color='#d80052'  # dots are pink
            )))
    # Safety
    fig.add_trace(
        go.Scattermapbox(
            visible=False,
            lat=safety_df.latitude,
            lon=safety_df.longitude,
            mode='markers',
            hovertemplate="<b>%{text}</b><br>" + "%{marker.size:,} report to feel unsafe during the lockdown" + "<extra></extra>",
            text=safety_df.area_name,
            marker=go.scattermapbox.Marker(
                sizeref=bubble_size,
                size=safety_df.safety,
                sizemode ="area",
                # size of the dots
                color='red'
            )))

    # Safety Change
    fig.add_trace(
        go.Scattermapbox(
            visible=False,
            lat=safety_change_df.latitude,
            lon=safety_change_df.longitude,
            mode='markers',
            hovertemplate="<b>%{text}</b><br>" + "%{marker.size:,} report to feel less safe during the lockdown" + "<extra></extra>",
            text=safety_change_df.area_name,
            marker=go.scattermapbox.Marker(
                sizeref=bubble_size,
                size=safety_change_df.safety_change,
                sizemode ="area",
                # size of the dots
                color='DarkRed'
            )))

    # Mental Health
    fig.add_trace(
        go.Scattermapbox(
            visible=False,
            lat=mental_health_df.latitude,
            lon=mental_health_df.longitude,
            mode='markers',
            hovertemplate="<b>%{text}</b><br>" + "%{marker.size:,} report to have a low mental health during the lockdown" + "<extra></extra>",
            text=mental_health_df.area_name,
            marker=go.scattermapbox.Marker(
                sizeref=bubble_size,
                size=mental_health_df.mental_health,
                sizemode ="area",
                # size of the dots
                color='orange'
            )))

    # Working situation
    fig.add_trace(
        go.Scattermapbox(
            visible=False,
            lat=working_situation_df.latitude,
            lon=working_situation_df.longitude,
            mode='markers',
            hovertemplate="<b>%{text}</b><br>" + "%{marker.size:,} report that they had to stop working during the lockdown" + "<extra></extra>",
            text=working_situation_df.area_name,
            marker=go.scattermapbox.Marker(
                sizeref=bubble_size,
                size=working_situation_df.working_situation,
                sizemode ="area",
                # size of the dots
                color='Indigo'
            )))

    fig.update_layout(  # mapbox_style="carto-positron",  # Chooses the type of map in the background
        paper_bgcolor='rgba(0,0,0,0)',
        height=580,  # height of the graph
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=30, t=20, b=20),
        mapbox=dict(accesstoken=token,
                    style=style_url,
                    center=go.layout.mapbox.Center(lat=54.237933, lon=-2.36967),
                    zoom=4.5  # add a zoom of size of great britain
                    ),
        updatemenus=[dict(
            xanchor="right",
            x=1,  # place of the menu
            borderwidth=0.1,
            buttons=list([
                dict(label="All reports",
                     method="update",
                     args=[{"visible": [True, False, False, False, False]}]),
                dict(label="Low Safety",
                     method="update",
                     args=[{"visible": [False, True, False, False, False]}]),
                dict(label="Safety Change for Worse",
                     method="update",
                     args=[{"visible": [False, False, True, False, False]}]),
                dict(label="Low Mental Health Rating",
                     method="update",
                     args=[{"visible": [False, False, False, True, False]}]),
                dict(label="Critical Working Situation",
                     method="update",
                     args=[{"visible": [False, False, False, False, True]}])
            ]),
        )])

    return fig
