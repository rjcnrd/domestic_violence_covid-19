
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import random
import pandas as pd

MESSAGES_DISPLAYED = 9
""" 
def get_messages(survey_df):
    all_reports = survey_df.written_report.tolist()
    random.shuffle(all_reports)
    first_x_reports_after_shuffle = all_reports[0:MESSAGES_DISPLAYED]
    return first_x_reports_after_shuffle """

def get_messages(survey_df):
    '''
    for styling
    '''
    report_list = pd.read_csv("https://raw.githubusercontent.com/rjcnrd/domestic_violence_covid-19/master/dummy-testimonials.csv").testimonials.tolist()
    return report_list


def create_testimonials_tab(survey_df):
    list_of_messages = get_messages(survey_df)
    tab_content = [
        dbc.Row([
            dbc.Col(html.P(list_of_messages[0]),md=6,className='text-truncate text-wrap'),
            dbc.Col(html.P(list_of_messages[1]),md=6)
        ]),
        dbc.Row([
            dbc.Col(html.P(list_of_messages[2]),md=3),
            dbc.Col(html.P(list_of_messages[3]),md=3),
            dbc.Col(html.P(list_of_messages[4]),md=3),
            dbc.Col(html.P(list_of_messages[5]),md=3)
        ]),
        dbc.Row([
            dbc.Col(html.P(list_of_messages[6]),md=4),
            dbc.Col(html.P(list_of_messages[7]),md=4),
            dbc.Col(html.P(list_of_messages[8]),md=4)
        ])]
    return tab_content
