# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layout import create_layout

#import pandas as pd
import logging

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('dummy-data.csv')
#logging.info(dummy_data_df)
#print("DEBUG",df)

colors = {
    'background': '#00a0dd',
    'text': '#fff'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = create_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
