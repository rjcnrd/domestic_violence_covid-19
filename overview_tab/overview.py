import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from overview_tab.map_graph import map_graph
from overview_tab.cumulative_nb_report import cumulative_graph


def create_overview_tab(df, postal_code_df, map_threshold):
    tab_content = html.Div(
        [
            dbc.Row([
                #Column 1: Left Side
                dbc.Col(
                    html.Div([
                        dcc.Graph(figure=map_graph(df, postal_code_df, map_threshold))
                        ])
                ),
                #Column 2: Right Side 
                dbc.Col(
                    html.Div([dcc.Graph(figure=cumulative_graph(df))
                    ])
                )
            ]),
        
        ])

    return tab_content


