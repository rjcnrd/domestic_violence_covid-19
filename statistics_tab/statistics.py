import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from statistics_tab.scatterplot_per_day import draw_scatterplot_per_day


def create_statistics_tab(survey_df):
    tab_content = html.Div([
        dbc.Row([
            html.H4(children=html.Span('This is how many of you got in touch with us in the past month',
                                       className="graph-heading-span"),
                    className="graph-heading"),
            html.Div([dcc.Graph(figure=draw_scatterplot_per_day(survey_df), responsive=True
                                )])]),
        dbc.Row(
            # for Roberta
        ),
        dbc.Row(
            # for Amélie
        )])

    return tab_content
