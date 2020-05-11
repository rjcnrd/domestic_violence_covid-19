import plotly.graph_objects as go
import numpy as np
import pandas as pd

COLORSCALE = ["white", "#d80052"]
FAMILY = "PT Sans"

graph1_df = pd.read_csv("./typeform/data_graph1.csv")


def add_ranking(survey_df):
    """
    adds a rank between (1, #of entries / day) to every report
    :param survey_df: df with a column "submitted_at"
    :returns: a df that has a new column "rankings"
    """
    survey_df.submitted_at = pd.to_datetime(survey_df.submitted_at)
    survey_df["submitted_at_day"] = survey_df.submitted_at.dt.strftime('%Y/%m/%d')
    survey_df["row_number"] = np.arange(len(survey_df))
    survey_df["ranking"] = survey_df.groupby(survey_df.submitted_at_day)["row_number"].rank(ascending=True)
    survey_df.submitted_at_day = pd.to_datetime(survey_df.submitted_at_day)
    return survey_df


def draw_scatterplot_per_day(survey_df):
    #PATCH
    survey_df = graph1_df

    df = add_ranking(survey_df)
    figure = go.Figure(data=go.Scatter(
        x=df.submitted_at_day,
        y=df.ranking,
        hovertemplate="%{text}" +
                      "<extra></extra>",


     
        text=df.testimonial,
        hoverlabel=dict(
            bgcolor="#00a0dd"),
        mode='markers',
        marker=dict(
            #size=10,
            color= df.display_testimonial,
            colorscale=COLORSCALE,
            opacity=0.7
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
