import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from overview_tab.map_graph import map_graph
from overview_tab.cumulative_nb_report import cumulative_graph
from overview_tab.survivors_report import first_time_assault_count, first_time_assault_percentage, agressor


def create_overview_tab(survey_df, all_reports_df, safety_df, safety_change_df, mental_health_df, working_situation_df,
                        big_bubble_size, small_bubble_size):
    tab_content = html.Div([

        dbc.Row([
            # Column 1: Left Side
            dbc.Col([
                html.H4(children=html.Span("Women all over the UK are experiencing difficulties during COVID-19",
                                           className="graph-heading-span"),
                        className="graph-heading"
                        ),
                html.Div(children=[
                    html.Div(children=[
                        dcc.Graph(figure=map_graph(
                            all_reports_df, safety_df, safety_change_df, mental_health_df, working_situation_df,
                            big_bubble_size, small_bubble_size))])

                ])
            ], md=6),
            # Column 2: Right Side
            dbc.Col([
                html.Div(
                    [html.H4(children=html.Span("Many of you have been in touch since we started our campaign",
                                                className="graph-heading-span"),
                             className="graph-heading"
                             ),
                     html.Div(children=
                              html.Div(children=[dcc.Graph(figure=cumulative_graph(survey_df))]))
                     ]),
                html.Div([
                    html.H4(children=html.Span("This is what you told us about your experience during COVID-19",
                                               className="graph-heading-span"),
                            className="graph-heading"
                            ),
                    dbc.Row([
                        dbc.Col(html.Div([html.Span(first_time_assault_count(survey_df), className="overviewNumber"),
                                          html.P("of you told us about feeling unsafe at home during the lockdown",
                                                 className="overviewText")],
                                         className="overviewSurvivorContainer")),
                        dbc.Col(
                            html.Div([html.Span(first_time_assault_percentage(survey_df), className="overviewNumber"),
                                      html.P("of you tell us they are anxious and/or depressed",
                                             className="overviewText")],
                                     className="overviewSurvivorContainer"))
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div([html.Span(agressor(survey_df, "partner"), className="overviewNumber"),
                                          html.P("of you feel insecure about the future",
                                                 className="overviewText")],
                                         className="overviewSurvivorContainer")),
                        dbc.Col(html.Div([html.Span(agressor(survey_df, "father"), className="overviewNumber"),
                                          html.P("of you are afraid of the future economic situation",
                                                 className="overviewText")],
                                         className="overviewSurvivorContainer"))
                    ])
                ])
            ], md=6)

        ])

    ])

    return tab_content
