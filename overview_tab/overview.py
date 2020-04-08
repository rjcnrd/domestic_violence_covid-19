import dash_core_components as dcc
from overview_tab.map_graph import map_graph
import dash_html_components as html
from overview_tab.cumulative_nb_report import cumulative_graph


def create_overview_tab(df, postal_code_df, map_threshold):
    tab_content = html.Div([
        html.Div(children=[
            html.Div(children=
                     html.Span("Number of incidents reported per postal code", className="graph-heading-span"),
                     className="graph-heading"
                     ),
            html.Div([
                dcc.Graph(figure=map_graph(df, postal_code_df, map_threshold)),
            ])],
            style={'width': '48%', 'display': 'inline-block'}),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=
                         html.Span("Cumulative number of incidents reported", className="graph-heading-span"),
                         className="graph-heading"
                         ),
                html.Div([dcc.Graph(figure=cumulative_graph(df))],
                         )])],
            style={'width': '48%', 'align': 'right', 'display': 'inline-block'})])

    return tab_content
