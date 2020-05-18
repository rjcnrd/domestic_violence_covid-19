import pandas as pd
import plotly.graph_objects as go

sankey_df=pd.read_csv("data/sankey.csv")

def sankey_graph():
    subdf=sankey_df
    
    living_dim = go.parcats.Dimension(
        values=subdf.living_category_var_names,
        categoryorder='category ascending', label="I am living with... ", ticktext=['perished', 'survived', '', '', '', '', '']
    )

    household_dim = go.parcats.Dimension(values=subdf.housework_mapped, label="I take care of ...",
                                        categoryarray=[0, 1, 2],
                                        ticktext=['all or most<br>of the <br>housework',  
                                                'as much<br>housework<br>as others',
                                                'less then other or none of the housework',
                                                ]
                                        )


    # Create parcats trace
    color = subdf.housework_mapped
    colorscale = 'agsunset'

    fig = go.Figure(data=[go.Parcats(
        dimensions=[living_dim, household_dim],

        line={'color': color, 'colorscale': colorscale},
        hoveron='color', hoverinfo='count',
        # labelfont={'size': 18, 'family': 'Times'},
        #tickfont={'size': 16, 'family': 'Times'},

    )])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,  # height of the graph
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=60, t=20, b=20),
    )



    return fig