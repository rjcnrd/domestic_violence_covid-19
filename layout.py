import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from overview_tab.overview import create_overview_tab
from statistics_tab.statistics import create_statistics_tab
from testimonials_tab.testimonials import create_testimonials_tab

#DATA IN - dummy for now
df = pd.read_csv(
    "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/dummy-data.csv")

#DATA Postal Code - in the git for now
postal_code = pd.read_csv("ukpostcodes.csv")

TAB_STYLE = {
    'font-family': 'Arial, Helvetica, sans-serif',
    'font-size': '3vw',
    'background': '#00a0dd',
    'color': 'white',
    'border': 'none',
    'border-top': 'none',
}

SELECTED_STYLE = {
    'font-family': 'Arial, Helvetica, sans-serif',
    'font-size': '3vw',
    'background': '#d80052',
    'color': 'white',
    'border-top': 'none',
    'border': 'none',
}


def create_layout():
    layout = html.Div(style={
    }, children=[
        html.Div(children=[
            html.H1(children='Hello World')
        ]),

        dcc.Tabs(className="tabs", children=[
            dcc.Tab(label='OVERVIEW', children=[
                create_overview_tab(df, postal_code)],
                style=TAB_STYLE,
                selected_style=SELECTED_STYLE),

            dcc.Tab(label='STATISTICS', children=[
                create_statistics_tab()
            ], style=TAB_STYLE,
                selected_style=SELECTED_STYLE),
            dcc.Tab(label='TESTIMONIALS', children=[
                create_testimonials_tab()
            ], style=TAB_STYLE,
                selected_style=SELECTED_STYLE),
        ])
    ])
    return layout
