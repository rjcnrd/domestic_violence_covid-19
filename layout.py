import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd

from overview_tab.overview import create_overview_tab
from statistics_tab.statistics import create_statistics_tab
from testimonials_tab.testimonials import create_testimonials_tab

# DATA
survey_df = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/dummy_data_new.csv", index_col=0)
new_data = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/dummy_final_survey_real_postcode_answers.csv", index_col=0)
all_reports_df = pd.read_csv(
        "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/data_map_all_reports.csv")
safety_df = pd.read_csv(
        "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/data_map_safety_scale.csv")
safety_change_df = pd.read_csv(
        "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/data_map_safety_change.csv")
mental_health_df = pd.read_csv(
        "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/data_map_mental_health.csv")
working_situation_df = pd.read_csv(
        "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/data_map_working_situation.csv")

# geo data
## UK Postal codes
postal_code_df = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/postcode_uk.csv")
## International countries
countries_df = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/countries.csv")

# variables for map chart
## Bubble size on the map graph (the bigger the number, the smaller the bubble). Size of markers for the first layer of the map graph (the overview)
BIG_BUBBLE_SIZE = 0.1
## Size for the other layers of the graph
SMALL_BUBBLE_SIZE = 0.01

# TAB STYLING
TAB_STYLE = {
    'background': '#00a0dd',
    'color': 'white',
    'border': 'none',
    'border-top': 'none',
    'font-family': 'BUKA',
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
    'font-family': 'BUKA',
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
                    create_overview_tab(survey_df, all_reports_df, safety_df, safety_change_df, mental_health_df, working_situation_df, BIG_BUBBLE_SIZE, SMALL_BUBBLE_SIZE))
            ],
                style=TAB_STYLE,
                selected_style=SELECTED_STYLE),

            dcc.Tab(label='STATISTICS',
                    children=dbc.Container(
                        create_statistics_tab(survey_df, new_data)),
                    style=TAB_STYLE,
                    selected_style=SELECTED_STYLE),

            dcc.Tab(label='TESTIMONIALS',
                    children=[
                        dbc.Container(create_testimonials_tab(
                            survey_df), className="testimonialsFrame")
                    ],
                    style=TAB_STYLE,
                    selected_style=SELECTED_STYLE),
        ])
    ], className="DashContent")
    return layout
