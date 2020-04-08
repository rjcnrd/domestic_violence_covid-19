import dash_core_components as dcc
from overview_tab.map_graph import  map_graph


def create_overview_tab(df, postal_code_df, map_threshold):
    tab_content = dcc.Graph(
        figure= map_graph(df, postal_code_df, map_threshold)
    )
    return tab_content
