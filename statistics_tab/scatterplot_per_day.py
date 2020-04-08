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
    df_new = survey_df
    df_new.date_of_report = pd.to_datetime(df_new.date_of_report, format='%d/%m/%Y %I:%M %p')
    df_new["date_of_report_day"] = df_new.date_of_report.dt.strftime('%d/%m/%Y')
    df_new["row_number"] = np.arange(len(df_new))
    df_new["ranking"] = df_new.groupby(df_new.date_of_report.dt.floor("d"))["row_number"].rank(ascending=True)
    return df_new


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
