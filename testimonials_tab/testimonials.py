import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import math
import numpy as np

MESSAGES_DISPLAYED = 9

""" 
def get_messages(survey_df):
    all_reports = survey_df.written_report.tolist()
    random.shuffle(all_reports)
    first_x_reports_after_shuffle = all_reports[0:MESSAGES_DISPLAYED]
    return first_x_reports_after_shuffle 
"""


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
        size = round(np.random.normal(0.75, 0.1), 2)
    elif text_length < 50:
        size = round(np.random.normal(1.5, 0.1), 2)
    else:
        size = 1.5 * (math.exp(-0.0009 * text_length))
        size = round(np.random.normal(size, 0.1), 2)
    stringified = str(size) + "rem"
    return stringified


def get_messages(survey_df):
    """
    for styling
    """
    report_list = survey_df[survey_df.display_testimonial == 1].written_report.tolist()
    return report_list


def create_column_content(list_of_messages):
    """
    :param list_of_messages:  an array of strings
    :return: a list of three lists, each containing the dash core components to fill a column. 
    """
    messages_in_first_column = []
    messages_in_second_column = []
    messages_in_third_column = []
    for index, message in enumerate(list_of_messages):
        if index % 3 == 0:
            messages_in_first_column.append(
                html.P(message, style={
                    'font-size': get_fontsize(message)
                })
            )
        if index % 3 == 1:
            messages_in_second_column.append(
                html.P(message, style={
                    'font-size': get_fontsize(message)
                })
            )
        if index % 3 == 2:
            messages_in_third_column.append(
                html.P(message, style={
                    'font-size': get_fontsize(message)
                })
            )
    return messages_in_first_column, messages_in_second_column, messages_in_third_column


def create_testimonials_tab(survey_df):
    list_of_messages = get_messages(survey_df)
    messages_in_first_column, messages_in_second_column, messages_in_third_column = create_column_content(
        list_of_messages)

    tab_content = dbc.Row([
        dbc.Col(messages_in_first_column, md=4),
        dbc.Col(messages_in_second_column, md=4),
        dbc.Col(messages_in_third_column, md=4)
    ])

    return tab_content
