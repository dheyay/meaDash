from dash import html, dcc
import dash_bootstrap_components as dbc
from plots.plotting import *
from data_processing.data_processor import DataProcessor
import numpy as np

def generate_sidebar(pathname, channel_info):
    """
    Generate the sidebar components based on the current page pathname and channel information.

    Parameters:
    - pathname (str): The current page pathname.
    - channel_info (list): The list of channel information.

    Returns:
    - sidebar_components (list): The list of sidebar components.
    """
    # Common components for all pages
    sidebar_common = [
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
        html.Hr(style={'border': 'none', 'border-top': '1px solid', 'margin': '10px 0'}),
        html.Br()
    ]

    if pathname == "/page-1" or pathname == "/":
        # Page with signal plot and channel activity heatmap
        page_specific = [
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
                dbc.Label("Time Value (s) for activity heatmap:", className="mr-2"),
                dbc.Input(id='time-value-input', type='number', min=0, step=0.1, value=1, style={'width': '100px'}),
                dbc.Button("Confirm", id='confirm-button', n_clicks=1, color="primary", className="ml-2", style={'width': '100px'}),
            ], className="input-group"),
            html.Br()
        ]
    elif pathname == "/page-2":
        # Page with raster plot
        page_specific = []
    elif pathname == "/page-3":
        # Page with spiking rate plot
        page_specific = [
            dbc.Row([
                    dbc.Col(
                        dbc.InputGroup([
                            dbc.Label("Window Size for aggregate spike activity (s):", className="mr-2"),
                            dbc.Input(id='window-size-input', type='number', min=0, step=0.1, value=0.2, style={'width': '100px'}),
                            dbc.Button("Apply", id='apply-button', n_clicks=1, color="primary", className="ml-2", style={'width': '100px'}),
                        ], className="input-group"),
                    ),
                ])
        ]
    else:
        page_specific = []
    sidebar_components = sidebar_common + page_specific
    return sidebar_components

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

def page_2_layout(data_processor):
    time_vec = np.arange(data_processor.initial_signal[0].shape[0]) / data_processor.sampling_rate
    raster_plot_figure = plot_raster(data_processor.raster, time_vector=time_vec)
    return dbc.Col([
        html.H4("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'left', 'margin': '20px'}),
        dcc.Graph(id='raster-plot', figure=raster_plot_figure)], width=10)

def page_3_layout(data_processor):
    average_spiking_rate_figure = plot_average_spiking_rate(np.sum(data_processor.aggregate_raster_spike_counts(
        total=False), axis=0))
    return dbc.Col([
        html.H4("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'left', 'margin': '20px'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='average-spiking-rate-plot', figure=average_spiking_rate_figure)),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='firing-rate-plot')),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='power-spectral-density-plot')),
        ]),
    ],  width=10)
        
def create_layout(channel_info, data_processor):
    return html.Div(
        [
            dcc.Location(id='url', refresh=False),
            dbc.Row(
                [
                    dbc.Col(id='sidebar', className="sidebar", width=2),
                    dbc.Col(id='page-content', className="content", width=10)
                ],
                className="g-0",
            )
        ],
        style={'max-width': '100%'}
    )
