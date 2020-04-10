import dash_core_components as dcc
import dash_html_components as html

from statistics_tab.scatterplot_per_day import draw_scatterplot_per_day


def create_statistics_tab(survey_df):
    tab_content = [
        html.H4(children=
                 html.Span('This is how many of you got in touch with us in the past month', className="graph-heading-span"),
                 className="graph-heading"),
        dcc.Graph(
            figure=draw_scatterplot_per_day(survey_df),
            responsive=True
        )]
    return tab_content
