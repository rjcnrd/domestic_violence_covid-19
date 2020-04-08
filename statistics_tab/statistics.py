import dash_core_components as dcc

from statistics_tab.scatterplot_per_day import draw_scatterplot_per_day



def create_statistics_tab(df):
    tab_content = [
        html.Div(children='Hello Dash'),
        dcc.Graph(
            figure=draw_scatterplot_per_day(df),
            responsive=True
        )]
    return tab_content

