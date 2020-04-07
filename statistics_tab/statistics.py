import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

from statistics_tab.scatterplot_per_day import draw_scatterplot_per_day 

def create_statistics_tab(df):
    tab_content = dcc.Graph(
        figure = draw_scatterplot_per_day(df)
    )
    return tab_content
