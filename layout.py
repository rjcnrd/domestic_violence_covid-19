import dash
import dash_core_components as dcc
import dash_html_components as html

from overview_tab.overview import create_overview_tab
from statistics_tab.statistics import create_statistics_tab
from testimonials_tab.testimonials import create_testimonials_tab


def create_layout():
    layout = html.Div(style={
        'background': "white"
    }, children=[
        html.Div(children=[
            html.H1(children='Hello World')
        ]),

        dcc.Tabs([
            dcc.Tab(label='Overview', children=[
                create_overview_tab()]),

            dcc.Tab(label='Statistics', children=[
                create_statistics_tab()
            ]),
            dcc.Tab(label='Testimonials', children=[
                create_testimonials_tab()
            ]),
        ])
    ])
    return layout

