import plotly.graph_objects as go
import numpy as np
import pandas as pd

COLORSCALE = ["white", "white", "white", "#d80052", "white"]
FAMILY = "PT Sans"


def add_ranking(survey_df):
    """
    adds a rank between (1, #of entries / day) to every report
    :param survey_df: df with a column "date_of_report"
    :returns: a df that has a new column "rankings"
    """
    survey_df.date_of_report = pd.to_datetime(survey_df.date_of_report, format='%d/%m/%Y %I:%M %p')
    survey_df["date_of_report_day"] = survey_df.date_of_report.dt.strftime('%Y/%m/%d')
    survey_df["row_number"] = np.arange(len(survey_df))
    survey_df["ranking"] = survey_df.groupby(survey_df.date_of_report_day)["row_number"].rank(ascending=True)
    survey_df.date_of_report_day = pd.to_datetime(survey_df.date_of_report_day)
    return survey_df


def draw_scatterplot_per_day(survey_df):
    df = add_ranking(survey_df)
    figure = go.Figure(data=go.Scatter(
        x=df.date_of_report_day,
        y=df.ranking,
        hovertemplate="%{text}" +
                      "<extra></extra>",
        text=df.written_report,
        hoverlabel=dict(
            bgcolor="#00a0dd"),
        mode='markers',
        marker=dict(
            #size=40,
            color=np.random.randn(len(df)),
            colorscale=COLORSCALE,
            opacity=0.5
        )

    ),
        layout=dict(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                color="white",
                showgrid=False),

            yaxis=dict(color="white",
                       showgrid=False)

        )

    )
    return figure
