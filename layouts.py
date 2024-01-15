from dash import html, dcc
import dash_bootstrap_components as dbc
from plotting import *
from data_processor import DataProcessor
import numpy as np

def create_sidebar(channel_info):
    return dbc.Col(
        [
            dbc.Nav(
                [
                    dbc.NavLink("Channel activity", href="/page-1", id="page-1-link", active="exact"),
                    dbc.NavLink("Raster plot", href="/page-2", id="page-2-link", active="exact"),
                    dbc.NavLink("Spiking rate/Firing Rate", href="/page-3", id="page-3-link", active="exact"),
                ],
                vertical=True,
                pills=True,
                className="mb-3",
            ),
            html.Br(),
            html.Hr(style={'border': 'none', 'border-top': '1px solid', 'margin': '10px 0'}),
            
            dcc.Dropdown(
                id='channel-dropdown',
                value=channel_info[0],
                options=[{'label': f'Channel {i}', 'value': i} for i in range(len(channel_info))],
                placeholder='Select a Channel'
            ),
            html.Br(),
            dcc.RadioItems(
                id='plot-type-selector',
                options=[
                    {'label': 'Initial Signal', 'value': 'initial'},
                    {'label': 'Raster Plot', 'value': 'raster'}
                ],
                value='initial'
            ),
            html.Br(),
            dbc.InputGroup([
                dbc.Label("Time Value (s) for spike activity:", className="mr-2"),
                dbc.Input(id='time-value-input', type='number', min=0, step=0.1, value=1, style={'width': '100px'}),
                dbc.Button("Confirm", id='confirm-button', n_clicks=1, color="grey", className="ml-2", style={'width': '100px'}),
            ], className="input-group"),
            html.Br()
        ],
        width=2,
        className="sidebar"
    )

def page_1_layout():
    return dbc.Col(
        [   
            html.H4("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'left', 'margin': '20px'}),
            dcc.Graph(id='channel-plot'),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='spike-activity-heatmap'), 
                            style={'resize': 'both', 'paddingLeft': '150px', 'overflow': 'auto'}, 
                            align="center"),
                    dbc.Col(dcc.Graph(id='spike-frequency-heatmap'))
                ]
            ),
        ]
    )

def page_2_layout():
    return dbc.Col([
        html.H4("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'left', 'margin': '20px'}),
        dcc.Graph(id='raster-plot')], width=10)

def page_3_layout():
    return dbc.Col([
        html.H4("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'left', 'margin': '20px'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='average-spiking-rate-plot')),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Spiking-rate-plot')),
        ])
    ],  width=10)
        
def create_layout(channel_info):
    return html.Div(
        [
            dcc.Location(id='url', refresh=False),
            dbc.Row(
                [
                    create_sidebar(channel_info),
                    dbc.Col(id='page-content', className="content", width=10)
                ],
                className="g-0",  # Remove gap between columns
            )
        ],
        style={'max-width': '100%'}
    )
