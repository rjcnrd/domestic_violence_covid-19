import pandas as pd
import plotly.graph_objects as go
import numpy as np
import warnings
from dotenv import load_dotenv
import os

load_dotenv()

warnings.filterwarnings("ignore", 'This pattern has match groups')
pd.options.mode.chained_assignment = None  # default='warn'

FAMILY = "PT Sans"
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MAPBOX_STYLE_URL = os.getenv("MAPBOX_STYLE_URL")


def postal_code_treatment(survey_data, postal_code_col="postal_code"):
    """
    :param survey_data: survey data
    :param postal_code_col: the name of the postal code column in the survey data
    :return: the survey data frame with the rows that start with a letter and contain a number. + Append to this data frame a column with the 2 first letters of the postal code : this is the name of the area and will be used in the join with the postal code data frame.
    """
    # Deletes the spacing at the beginning
    survey_data[postal_code_col] = survey_data[postal_code_col].str.lstrip()
    survey_data[postal_code_col] = survey_data[postal_code_col].str.upper()

    # Start with a letter and Contains a number
    data_to_display = survey_data.loc[survey_data[postal_code_col].str.contains('(^[A-Z])(.*\d+)', na=False)]
    data_to_display["area"] = data_to_display[postal_code_col].str.extract('^(\D*)')
    data_to_display["area"] = data_to_display["area"].str.rstrip()
    return data_to_display


def country_treatment(survey_data, countries_df, postal_code_col="postal_code"):
    """
    :param survey_data: survey data
    :param countries_df: latitude and longitude of the international countries
    :param postal_code_col: the name of the postal code column in the survey data
    :return: the survey data frame with the rows where the postal code is simply the name of the country (with or without spacing). + Append to this data frame a column the name of the country : this is the name of the area and will be used in the join with the country data frame
    """
    # Deletes the spacing at the beginning
    survey_data.loc[:, postal_code_col] = survey_data.loc[:, postal_code_col].str.lstrip()
    survey_data.loc[:, postal_code_col] = survey_data.loc[:, postal_code_col].str.upper()
    survey_data.loc[:, postal_code_col] = survey_data.loc[:, postal_code_col].str.lstrip()

    # Start with a letter and Contains a number
    data_to_display = survey_data.loc[survey_data.loc[:, postal_code_col].isin(countries_df.country_name)]
    data_to_display = data_to_display.reset_index().merge(countries_df[["area", "country_name"]], how="left",
                                                          right_on="country_name", left_on=postal_code_col).drop(
        columns=["country_name"]).set_index('index')
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
    :param survey_df: data from the survey
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :param postal_code_df: data frame that includes the postal codes, the latitude and the longitude
    :return: 5 dataframe with one row per postal code as index, with latitude, longitude and number of incidents
    """
    safety = pd.DataFrame(survey_df.loc[survey_df.safety_level < 3].groupby("area")["safety_level"].count())
    safety = apply_threshold_merge_postcode(safety, "safety_level", postal_code_df, map_threshold)

    safety_change = pd.DataFrame(
        survey_df.loc[survey_df.safety_change == "Worse"].groupby("area")["safety_change"].count())
    safety_change = apply_threshold_merge_postcode(safety_change, "safety_change", postal_code_df, map_threshold)

    mental_health = pd.DataFrame(survey_df.loc[survey_df.mental_scale < 3].groupby("area")["mental_scale"].count())
    mental_health = apply_threshold_merge_postcode(mental_health, "mental_scale", postal_code_df, map_threshold)

    working_situation = pd.DataFrame(
        survey_df.loc[survey_df.work_situation.isin(["No, I have been furloughed because of the lockdown",
                                                     "No, I have been made redundant because of the lockdown",
                                                     "No, I have had to stop working for other reasons related to COVID-19"])].groupby(
            "area")["work_situation"].count())
    working_situation = apply_threshold_merge_postcode(working_situation, "work_situation", postal_code_df,
                                                       map_threshold)

    all_reports = pd.DataFrame(survey_df.groupby("area")["safety_level"].count())
    all_reports = all_reports.rename(columns={"safety_level": "all_reports"})
    all_reports = apply_threshold_merge_postcode(all_reports, "all_reports", postal_code_df, map_threshold)
    all_reports = all_reports.merge(safety[["safety_level", "area"]], left_on="area", right_on="area",
                                    how="left")
    all_reports = all_reports.merge(safety_change[["safety_change", "area"]], left_on="area", right_on="area",
                                    how="left")
    all_reports = all_reports.merge(mental_health[["mental_scale", "area"]], left_on="area", right_on="area",
                                    how="left")
    all_reports = all_reports.merge(working_situation[["work_situation", "area"]], left_on="area",
                                    right_on="area", how="left")
    all_reports.safety_level = all_reports.safety_level.fillna(-1).astype(int).astype(str).replace('-1', np.nan)
    all_reports.safety_change = all_reports.safety_change.fillna(-1).astype(int).astype(str).replace('-1', np.nan)
    all_reports.mental_scale = all_reports.mental_scale.fillna(-1).astype(int).astype(str).replace('-1', np.nan)
    all_reports.work_situation = all_reports.work_situation.fillna(-1).astype(int).astype(str).replace('-1', np.nan)
    all_reports[["safety_level", "safety_change", "mental_scale", "work_situation"]] = all_reports[
        ["safety_level", "safety_change", "mental_scale", "work_situation"]].fillna("0")
    return all_reports, safety, safety_change, mental_health, working_situation


def merge_local_internat_dataframe(survey_df, postal_code_df, countries_df, postal_code_col, map_threshold):
    """
    :param postal_code_col: string with the name of the postal code column
    :param countries_df: latitude and longitude of the international countries
    :param map_threshold: a number giving the threshold after which we can plot a marker on the map
    :param survey_df: dummy data
    :param postal_code_df: postal code data frame
    :return: merge the output of the data_processing_for_graph for UK postcodes and for the international. Output is given to the map function + Returns the data that is not in the data frame
    """
    # UK postcodes
    uk_data = postal_code_treatment(survey_df, postal_code_col=postal_code_col)

    # Include the ones that provide directly the name of the county
    postal_code_df["upper"] = postal_code_df["area_name"].str.upper()
    uk_data_county = survey_df.reset_index().merge(postal_code_df, left_on="location", right_on="upper").drop(
        columns=["area_name", "latitude", "longitude", "upper"]).set_index('index')
    uk_data = uk_data.append(uk_data_county)

    # Do the processing for the UK data
    all_reports_uk, safety_uk, safety_change_uk, mental_health_uk, working_situation_uk = data_processing_for_graph(
        uk_data, postal_code_df, map_threshold)

    # Countries postcodes
    internat_data = country_treatment(survey_df, countries_df, postal_code_col=postal_code_col)
    all_reports_internat, safety_internat, safety_change_internat, mental_health_internat, working_situation_internat = data_processing_for_graph(
        internat_data, countries_df, map_threshold)

    # Return the data that is not on the map
    not_in_map = survey_df.drop(index=uk_data.index)
    not_in_map = not_in_map.drop(index=internat_data.index)

    # NOW NEED TO APPEND ONE UNDER THE OTHER
    all_reports = all_reports_uk.append(all_reports_internat)
    safety = safety_uk.append(safety_internat)
    safety_change = safety_change_uk.append(safety_change_internat)
    mental_health = mental_health_uk.append(mental_health_internat)
    working_situation = working_situation_uk.append(working_situation_internat)

    return all_reports, safety, safety_change, mental_health, working_situation, not_in_map, uk_data, uk_data_county


def map_graph(all_reports_df, safety_df, safety_change_df, mental_health_df, working_situation_df, big_bubble_size=2,
              small_bubble_size=0.01):
    """
    :param all_reports_df: a pandas df with the number of reports per location, and the details of the reports
    :param safety_df: a pandas df with the number of reports of safety issues per location
    :param safety_change_df: a pandas df with the number of reports of safety decrease per location
    :param mental_health_df: a pandas df with the number of reports of low mental health per location
    :param working_situation_df: a pandas df with the number of reports of people who had to stop to work per location
    :param big_bubble_size: size of the reference bubble in the map. For the first layer. The bigger the bubble_size, the smaller the bubble
    :param small_bubble_size: size of the reference bubble in the map. For the other layer. The bigger the bubble_size, the smaller the bubble
    :return: map of UK with the number of aggressions
    """

    # Text for hover
    all_reports_df["overall_text"] = np.where(all_reports_df["all_reports"] == 1,
                                              all_reports_df["all_reports"].map("<b>{} report from ".format) +
                                              all_reports_df["area_name"].map("{} </b>".format),
                                              all_reports_df["all_reports"].map("<b>{} reports from ".format) +
                                              all_reports_df["area_name"].map("{} </b>".format))
    all_reports_df["safety_text"] = np.where(all_reports_df["safety_level"] == 0,
                                             "",
                                             np.where(all_reports_df["safety_level"] == 1,
                                                      all_reports_df["safety_level"].map(
                                                          "<br><i>{}</i> reports to feel unsafe".format),
                                                      all_reports_df["safety_level"].map(
                                                          "<br><i>{}</i> report to feel unsafe".format)))
    all_reports_df["safety_change_text"] = np.where(all_reports_df["safety_change"] == 0,
                                                    "",
                                                    np.where(all_reports_df["safety_change"] == 1,
                                                             all_reports_df["safety_change"].map(
                                                                 "<br><i>{}</i> reports feeling less safe".format),
                                                             all_reports_df["safety_change"].map(
                                                                 "<br><i>{}</i> report feeling less safe".format)))
    all_reports_df["mental_scale_text"] = np.where(all_reports_df["mental_scale"] == 0,
                                                   "",
                                                   np.where(all_reports_df["mental_scale"] == 1,
                                                            all_reports_df["mental_scale"].map(
                                                                "<br><i>{}</i> reports low mental health".format),
                                                            all_reports_df["mental_scale"].map(
                                                                "<br><i>{}</i> report low mental health".format)))
    all_reports_df["work_situation_text"] = np.where(all_reports_df["work_situation"] == 0,
                                                     "",
                                                     np.where(all_reports_df["work_situation"] == 1,
                                                              all_reports_df["work_situation"].map(
                                                                  "<br><i>{}</i> reports that they had to stop working".format),
                                                              all_reports_df["work_situation"].map(
                                                                  "<br><i>{}</i> report that they had to stop working".format)))

    # All reports
    fig = go.Figure(
        data=go.Scattermapbox(
            lat=all_reports_df.latitude,
            lon=all_reports_df.longitude,
            mode='markers',
            hovertemplate="%{customdata[0]}" +
                          "%{customdata[1]}" +
                          "%{customdata[2]}" +
                          "%{customdata[3]}" +
                          "%{customdata[4]}" +
                          "<extra></extra>",
            hoverlabel=dict(bgcolor='#eceded',
                            bordercolor='#eceded',
                            font=dict(color="rgb(68, 68, 68)", size=11)),
            customdata=np.stack(
                (all_reports_df["overall_text"], all_reports_df["safety_text"], all_reports_df["safety_change_text"],
                 all_reports_df["mental_scale_text"], all_reports_df["work_situation_text"]), axis=-1),
            marker=go.scattermapbox.Marker(
                sizeref=big_bubble_size,
                size=all_reports_df.all_reports,
                sizemode="area",
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
            hoverlabel=dict(bgcolor='#eceded',
                            bordercolor='#eceded',
                            font=dict(color="rgb(68, 68, 68)", size=11)),
            marker=go.scattermapbox.Marker(
                sizeref=small_bubble_size,
                size=safety_df.safety_level,
                sizemode="area",
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
            hoverlabel=dict(bgcolor='#eceded',
                            bordercolor='#eceded',
                            font=dict(color="rgb(68, 68, 68)", size=11)),
            marker=go.scattermapbox.Marker(
                sizeref=small_bubble_size,
                size=safety_change_df.safety_change,
                sizemode="area",
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
            hoverlabel=dict(bgcolor='#eceded',
                            bordercolor='#eceded',
                            font=dict(color="rgb(68, 68, 68)", size=11)),
            marker=go.scattermapbox.Marker(
                sizeref=small_bubble_size,
                size=mental_health_df.mental_scale,
                sizemode="area",
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
            hoverlabel=dict(bgcolor='#eceded',
                            bordercolor='#eceded',
                            font=dict(color="rgb(68, 68, 68)", size=11)),
            marker=go.scattermapbox.Marker(
                sizeref=small_bubble_size,
                size=working_situation_df.work_situation,
                sizemode="area",
                # size of the dots
                color='Indigo'
            )))

    fig.update_layout(  # mapbox_style="carto-positron",  # Chooses the type of map in the background
        paper_bgcolor='rgba(0,0,0,0)',
        height=580,  # height of the graph
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=30, t=20, b=20),
        mapbox=dict(accesstoken=MAPBOX_TOKEN,
                    style=MAPBOX_STYLE_URL,
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
