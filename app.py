# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc

from layout import create_layout

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div class="head-of-app"><H1>Test Dashboard</H1></div>
        <div class="app-entry">        
        {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div> </div>
    </body>
</html>
'''

app.layout = dbc.Container(
    create_layout()
    ,className="app-entry")

if __name__ == '__main__':
    app.run_server(debug=True)
