import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd

from overview_tab.overview import create_overview_tab
from statistics_tab.statistics import create_statistics_tab
from testimonials_tab.testimonials import create_testimonials_tab

# DATA IN - dummy for now
survey_df = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/dummy_data_new.csv",
                        index_col=0)

new_data = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/dummy_final_survey.csv", index_col = 0)

# DATA Postal Code - in the git for now
postal_code_df = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/ukpostcodes.csv")

# Threshold for plotting the data in the graph
map_threshold = 2

#Bubble size on the map graph (the bigger the smaller the bubble)
bubble_size = 2

# TAB STYLE IS EQUAL  to H3 in default style
TAB_STYLE = {
    'background': '#00a0dd',
    'color': 'white',
    'border': 'none',
    'border-top': 'none',
    'font-family':'BUKA',
    'font-size': '6rem',
    'text-transform': 'uppercase',
    'letter-spacing': ' 3px',
    'margin-top': '0',
    'margin-bottom': '0.5rem',
    'font-weight': '600',
    'line-height': '1.2',
}

SELECTED_STYLE = {
    'background': '#00a0dd',
    'color': '#d80052',
    'border-top': 'none',
    'border': 'none',
      'font-family':'BUKA',
    'font-size': '6rem',
    'text-transform': 'uppercase',
    'letter-spacing': ' 3px',
    'margin-top': '0',
    'margin-bottom': '0.5rem',
    'font-weight': '600',
    'line-height': '1.2',
}


def create_layout():
    layout = html.Div(style={
    }, children=[
        dcc.Tabs(className="tabs", children=[

            dcc.Tab(label='OVERVIEW', children=[
                dbc.Container(
                    create_overview_tab(survey_df, new_data, postal_code_df, map_threshold, bubble_size))
            ],
                    style=TAB_STYLE,
                    selected_style=SELECTED_STYLE),

            dcc.Tab(label='STATISTICS',
                    children=dbc.Container(create_statistics_tab(survey_df, new_data)),
                    style=TAB_STYLE,
                    selected_style=SELECTED_STYLE),

            dcc.Tab(label='TESTIMONIALS',
                    children=[
                        dbc.Container(create_testimonials_tab(survey_df), className="testimonialsFrame")
                    ],
                    style=TAB_STYLE,
                    selected_style=SELECTED_STYLE),
        ])
    ],className="DashContent")
    return layout
