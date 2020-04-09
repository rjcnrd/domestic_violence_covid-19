import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from overview_tab.map_graph import map_graph
from overview_tab.cumulative_nb_report import cumulative_graph


def create_overview_tab(df, postal_code_df, map_threshold):
    tab_content = dbc.Row([
        # Column 1: Left Side
        dbc.Col([
            html.H4(children=html.Span("Number of incidents reported per postal code", className="graph-heading-span"),
                    className="graph-heading"
                    ),
            html.Div([
                dcc.Graph(figure=map_graph(
                    df, postal_code_df, map_threshold))
            ])], md=6
        ),
        # Column 2: Right Side
        dbc.Col([
            html.Div(
                [html.H4(children=html.Span("Cumulative number of incidents reported", className="graph-heading-span"),
                         className="graph-heading"
                         ),
                 html.Div([dcc.Graph(figure=cumulative_graph(df))
                           ])
                 ]),
            html.Div([
                html.H4(children=html.Span("Survivors report", className="graph-heading-span"),
                        className="graph-heading"
                        ),
                dbc.Row([
                    dbc.Col(html.Div("One of two columns")),
                    dbc.Col(html.Div("One of two columns"))
                ]),
                dbc.Row([
                    dbc.Col(html.Div("One of two columns")),
                    dbc.Col(html.Div("One of two columns"))
                ])
            ])
        ], md=6)
    ])

    return tab_content
