import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from statistics_tab.scatterplot_per_day import draw_scatterplot_per_day
from statistics_tab.scatter_bar_plot_mental_health import draw_scatterbarplot


def create_statistics_tab(survey_df, new_data):
    tab_content = html.Div([
        dbc.Row([
            html.H4(children=html.Span('This is how many of you got in touch with us in the past month',
                                       className="graph-heading-span"),
                    className="graph-heading"),
            html.Div([dcc.Graph(figure=draw_scatterplot_per_day(survey_df), responsive=True
                                )], style={'display': 'inline-block', 'width': '100%'})]),
        dbc.Row(
            # for Roberta
        ),
        dbc.Row([
            html.H4(children=html.Span('This is how you rate your mental heath during the lockdown',
                                       className="graph-heading-span"),
                    className="graph-heading"),
            html.Div([dcc.Graph(figure=draw_scatterbarplot(new_data, num_by_col=3), responsive=True
                                )], style={'display': 'inline-block', 'width': '100%'})]
        )])

    return tab_content
