import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from overview_tab.map_graph import map_graph
from overview_tab.cumulative_nb_report import cumulative_graph
from overview_tab.survivors_report import first_time_assault_count, first_time_assault_percentage, agressor


def create_overview_tab(survey_df, postal_code_df, map_threshold):
    tab_content = dbc.Row([
        # Column 1: Left Side
        dbc.Col([
            html.H4(children=html.Span("Number of incidents reported per postal code", className="graph-heading-span"),
                    className="graph-heading"
                    ),
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(figure=map_graph(
                        survey_df, postal_code_df, map_threshold))])

            ])
        ], md=6),
        # Column 2: Right Side
        dbc.Col([
            html.Div(
                [html.H4(children=html.Span("Cumulative number of incidents reported", className="graph-heading-span"),
                         className="graph-heading"
                         ),
                 html.Div(children=
                          html.Div(children=[dcc.Graph(figure=cumulative_graph(survey_df))]))
                 ]),
            html.Div([
                html.H4(children=html.Span("Survivors report", className="graph-heading-span"),
                        className="graph-heading"
                        ),
                dbc.Row([
                    dbc.Col(html.Div([html.Span(first_time_assault_count(survey_df), className="overviewNumber"),
                                      html.P("Women report being assaulted for the first time during the lockdown",
                                             className="overviewText")],
                                     className="overviewSurvivorContainer")),
                    dbc.Col(html.Div([html.Span(first_time_assault_percentage(survey_df), className="overviewNumber"),
                                      html.P("Women report being assaulted for the first time during the lockdown",
                                             className="overviewText")],
                                     className="overviewSurvivorContainer"))
                ]),
                dbc.Row([
                    dbc.Col(html.Div([html.Span(agressor(survey_df, "partner"), className="overviewNumber"),
                                      html.P("Women report being assaulted by their partner",
                                             className="overviewText")],
                                     className="overviewSurvivorContainer")),
                    dbc.Col(html.Div([html.Span(agressor(survey_df, "father"), className="overviewNumber"),
                                      html.P("Women report being assaulted by their father", className="overviewText")],
                                     className="overviewSurvivorContainer"))
                ])
            ])
        ], md=6)
    ])

    return tab_content
