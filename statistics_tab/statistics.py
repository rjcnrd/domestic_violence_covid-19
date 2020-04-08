import dash_core_components as dcc
import dash_html_components as html

from statistics_tab.scatterplot_per_day import draw_scatterplot_per_day

def create_statistics_tab(df):
    tab_content = [
        html.Div(children=
        html.Span('Number of incidents reported per day',className="graph-heading-span"),
        className="graph-heading"),
        dcc.Graph(
            figure=draw_scatterplot_per_day(df),
            responsive=True
        )]
    return tab_content

