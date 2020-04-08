import pandas as pd
import plotly.express as px

FAMILY = "PT Sans"


def data_processing_cumulative(survey_df):
    """
    :param survey_df: data of the number of reports. Using the date of report and the first_time_experience (but only for the groupby, could be another column)
    :return: a pandas data frame with the cumulative number of report per day
    """
    survey_df.date_of_report = pd.to_datetime(survey_df.date_of_report, format='%d/%m/%Y %I:%M %p')
    survey_df["date_of_report_day"] = survey_df.date_of_report.dt.strftime('%Y/%m/%d')
    survey_df = survey_df.sort_values(by="date_of_report_day")
    data = pd.DataFrame(survey_df.groupby("date_of_report_day")["first_time_experience"].count().cumsum())
    data = data.rename(columns={"first_time_experience": "cumulative_number_of_reports"}).reset_index()
    data.date_of_report_day = pd.to_datetime(data.date_of_report_day)
    return data


def cumulative_graph(survey_df):
    """
    :param survey_df:  data with the number of reports
    :return: the graph for the cumulative number of reports
    """
    data = data_processing_cumulative(survey_df)
    fig = px.area(data,
                  x="date_of_report_day",
                  y="cumulative_number_of_reports", color_discrete_sequence=["white"],
                  #width=600,  # width of the graph
                  #height=300
                   )  # height of the graph

    fig.update_layout(paper_bgcolor="#00a0dd",
                      plot_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(color="white", showgrid=False),
                      xaxis_title="Date",
                      yaxis_title="",
                      yaxis=dict(color="white", showgrid=False))

    return fig
