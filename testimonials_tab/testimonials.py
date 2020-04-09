import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import random
import pandas as pd
import math
import numpy as np

MESSAGES_DISPLAYED = 9

""" 
def get_messages(survey_df):
    all_reports = survey_df.written_report.tolist()
    random.shuffle(all_reports)
    first_x_reports_after_shuffle = all_reports[0:MESSAGES_DISPLAYED]
    return first_x_reports_after_shuffle """

def get_fontsize(testimonial):
    """
    this function determines a font size in rem
    default on page is: 0.875
    max is: 1.5
    min is: 0.75
    if text_length falls between limits rem is calculated by fitted exponential function
    random gaussian noise is added with mean = calculated size with a sd. of 0.1
    """
    text_length = len(testimonial)
    if text_length > 800: 
        size = np.random.normal(0.75,0.1) 
    elif text_length < 50: 
        size = np.random.normal(1.5,0.1) 
    else:
        size =  round(1.5*(math.exp(-0.0009*text_length)),2)
        size = np.random.normal(size,0.1) 
    
    stringified = str(size)+"rem"
    return stringified

def get_messages(survey_df):
    """
    for styling
    """
    report_list = pd.read_csv(
        "https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/data/dummy-testimonials.csv").testimonials.tolist()
    return report_list


def create_testimonials_tab(survey_df):
    list_of_messages = get_messages(survey_df)
    tab_content =         dbc.Row([
            dbc.Col([
                html.P(list_of_messages[1],style={
                    'font-size': get_fontsize(list_of_messages[1])
                    }),
                html.P(list_of_messages[2],style={
                'font-size': get_fontsize(list_of_messages[2])
                }),
                html.P(list_of_messages[3],style={
                'font-size': get_fontsize(list_of_messages[3])
                })
            ], md=4),


            dbc.Col([
                html.P(list_of_messages[3]),
                html.P(list_of_messages[4]),
                html.P(list_of_messages[5])
            ], md=4),

            dbc.Col([
                html.P(list_of_messages[6]),
                html.P(list_of_messages[7]),
                html.P(list_of_messages[8])
            ], md=4),
        ])
        
    return tab_content
