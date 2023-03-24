import dash
from dash import html as dhtml
from dash import dcc, Input, Output, State
from dash.dash_table.Format import Format, Scheme
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc

#non-plotly imports
import open_nc
import numpy as np
import pandas as pd

'''
========================================================================================================================
Data
'''

var_names = {'temp_max': 'tasmaxAdjust',
             'temp_min': 'tasminAdjust',
             'temp_mean': 'tasAdjust',
             'precip': 'prAdjust'}

human_names = {'temp_max':      'Temperature Max',
               'temp_min':      'Temperature Min',
               'temp_mean':     'Temperature Mean',
               'precip':        'Precipitation'}

dropdown_datasets = [#{'label':  '',     'value':   'none'},
             {'label':  'Temperature Max',     'value':   'temp_max'},
             {'label':  'Temperature Min',     'value':   'temp_min'},
             {'label':  'Temperature Mean',    'value':   'temp_mean'},
             {'label':  'Precipitation',       'value':   'precip'}
             ]

default_group = open_nc.multiVarNCSet('/home/shjewell/PycharmProjects/wait_five_minutes_weather/stats-20010101-20051231.nc', var_names)
df = default_group.ret_set('tasAdjust', 'mean')
lats = default_group.lats
lons = default_group.lons

'''
========================================================================================================================
Dashboard

There are two options for mapping: using the mapping functions in Plotly, but these are slow

And using a heatmap, which is fast. Maybe giving the user the option to switch between these would be good?
'''

graph_config = {'modeBarButtonsToRemove' : ['hoverCompareCartesian', 'select2d', 'lasso2d'],
                'doubleClick':  'reset+autosize', 'toImageButtonOptions': { 'height': None, 'width': None, },
                'displaylogo': False}

colors = {'background': '#111111', 'text': '#7FDBFF'}

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                external_stylesheets=[dbc.themes.SLATE])
#application = app.server
app.title = "Geospatial Analysis Dashboard"

# ts = go.Figure()
# ts.update_layout(paper_bgcolor='#515960', plot_bgcolor='#515960',
#                  font_color='white',
#                  margin=dict(l=5, r=5, t=5, b=5))

controls_card = dbc.Card(
    dbc.CardBody(id='analysis-card',
        children=[
            dcc.Dropdown(id='set-select', options=dropdown_datasets, value='temp_mean'),
            dcc.RadioItems(id='analysis-select',
                           options=[{'label':   'Max    ',  'value':     'max'},
                                    {'label':   'Min    ',  'value':     'min'},
                                    {'label':   'Mean   ',  'value':     'mean'},
                                    {'label':   'Median ',  'value':     'median'},
                                    {'label':   'Std Dev',  'value':     'std'}],
                           value='mean', inline=False)
            ])
)

wfm_map = go.Figure()
wfm_map.add_heatmap(x=lons, y=lats, z=default_group.ret_default_heuristic())
wfm_map.update_layout(paper_bgcolor='#515960', plot_bgcolor='#515960',
                  font_color='white',
                  margin=dict(l=5, r=5, t=5, b=5))

analysis_tab = dbc.Card(
    dbc.CardBody(children=[
        dbc.Row(children=[
            dbc.Col(
                children=[dcc.Loading(dcc.Graph(id='wfm-map', figure=wfm_map))],
                width=8
            ),
            dbc.Col(
                children=[
                    dhtml.H5('Daily Temperature Spread'),
                    dcc.Slider(id='temp-spread', max=1, min=0, value=1),
                    dhtml.H5('Variability of Precipitation'),
                    dcc.Slider(id='precip-var', max=1, min=0, value=0),
                    dhtml.H5('Variability of Temperature'),
                    dcc.Slider(id='temp-var', max=1, min=0, value=0),
                    dhtml.H5('Likelyhood of a Hot Day'),
                    dcc.Slider(id='temp-max-prob', max=1, min=0, value=0),
                    dhtml.H5('Likelyhood of a Cold Day'),
                    dcc.Slider(id='temp-min-prob', max=1, min=0, value=0)
                ]
            )
        ])
    ])
)

stats_map = go.Figure()
stats_map.add_heatmap(x=lons, y=lats, z=df, hovertemplate='Temp: %{z:.2f}°C<br>Lat: %{y:.2f}<br>Lon: %{x:.2f}')
stats_map.update_layout(paper_bgcolor='#515960', plot_bgcolor='#515960',
                  font_color='white',
                  margin=dict(l=5, r=5, t=5, b=5))

map_page = dbc.Card(
    dbc.CardBody(id='map_container',
        children=[
            dbc.Row([
                dbc.Col(
                    children=[
                        dhtml.H5('Mean of Daily Mean Temperature, 2001-01-01 to 2005-12-31', id='map-label'),
                        dcc.Loading(dcc.Graph(id='mapbox', figure=stats_map))],
                        width=8),
                dbc.Col(controls_card, width=4)
            ])
        ]
    )
)


app.layout = dhtml.Div([
    dcc.Tabs(
        children=[
            dcc.Tab(id='stats-tab', label='Weather Stats',
                    children=[dbc.Card(map_page)]),
            dcc.Tab(id='analysis-tab', label='Analysis Tab',
                    children=[dbc.Card(analysis_tab)])
            ]
    ),
    dcc.Link('By SHJewell', href=f'https://shjewell.com'),
    dhtml.H6(f'Built using Python and Plotly Dash'),
    dcc.Link('Source code', href=f'https://github.com/SHJewell/wait_five_minutes_weather')
])

'''
========================================================================================================================
Callbacks
'''

@app.callback(
    [Output('mapbox', 'figure'),
     Output('map-label', 'children')],
    [Input('set-select', 'value'),
     Input('analysis-select', 'value')]
)
def update_map(set, analysis):

    new_df = default_group.ret_set(var_names[set], analysis)
    lats = default_group.lats
    lons = default_group.lons

    hovertxt = 'Precip: %{z:.5f} kg m-2 s-1<br>Lat: %{y:.2f}<br>Lon: %{x:.2f}'

    if 'temp' in set:
        hovertxt = 'Temp: %{z:.2f}K<br>Lat: %{y:.2f}<br>Lon: %{x:.2f}'

    map = go.Figure(data=go.Heatmap(x=lons, y=lats, z=new_df,
                                    hovertemplate=hovertxt))
    map.update_layout(paper_bgcolor='#515960', plot_bgcolor='#515960',
                      font_color='white',
                      margin=dict(l=5, r=5, t=5, b=5))

    a_label =  f'{analysis[0].upper()}{analysis[1:]}'
    map_label = f'{a_label} of {human_names[set]},  2001-01-01 to 2005-12-31'

    return map, map_label

@app.callback(
    Output('wfm-map', 'figure'),
    [Input('temp-spread', 'value'),
     Input('precip-var', 'value'),
     Input('temp-var', 'value'),
     Input('temp-max-prob', 'value'),
     Input('temp-min-prob', 'value')]
)
def wait_five_minutes(t_spread, p_var, t_var, t_maxp, t_minp):

    heuristic = default_group.ret_default_heuristic()

    total_weight = t_spread + p_var + t_var + t_maxp + t_minp

    if t_spread != 0:
        heuristic = heuristic * (t_spread / total_weight)
    if p_var != 0:
        heuristic = heuristic + (default_group.data['prAdjust_std'] / np.nanmax(default_group.data['prAdjust_std']))

    hrstc_df = heuristic

    wfm_fig = go.Figure()
    wfm_fig.add_heatmap(x=default_group.lons, y=default_group.lats, z=hrstc_df)
    wfm_fig.update_layout(paper_bgcolor='#515960', plot_bgcolor='#515960',
                          font_color='white',
                          margin=dict(l=5, r=5, t=5, b=5))

    return wfm_fig

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)
    #application.run(port=8080)
