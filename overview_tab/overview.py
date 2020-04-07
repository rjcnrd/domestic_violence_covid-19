import dash_core_components as dcc
from overview_tab.map_graph import map_graph
import dash_html_components as html
from overview_tab.cumulative_nb_report import cumulative_graph


def create_overview_tab(df, postal_code_df, threshold):
    tab_content = html.Div([dcc.Graph(figure=map_graph(df, postal_code_df, threshold)),
                            dcc.Graph(figure=cumulative_graph(df))])
    return tab_content
