import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from plotting import *
from data_processor import DataProcessor
from plotting import *
from data_processor import DataProcessor


import plotly.graph_objects as go

def create_dropdown_options(channel_info):
    return [{'label': f'Channel {i}', 'value': i} for i in range(len(channel_info))]

def create_app_layout(channel_info):
    return html.Div([
        html.H2("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'left', 'margin': '30px'}),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='channel-dropdown',
                value=channel_info[0],
                options=create_dropdown_options(channel_info),
                placeholder='Select a Channel'
            ), width={'size': 4, 'offset': 3}, style={'margin': '30px'}),
            dbc.Col(dcc.RadioItems(
                id='plot-type-selector',
                options=[
                    {'label': 'Initial Signal', 'value': 'initial'},
                    {'label': 'Raster Plot', 'value': 'raster'}
                ],
                value='initial'
            ), width={'size': 4, 'offset': 0}, style={'margin': '10px'}),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='channel-plot'), md=12),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='raster-plot'), style={'resize': 'both', 'overflow': 'auto'}),
        ]),
        dbc.Row([
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Graph(id='spike-activity-heatmap', style={'resize': 'both', 'overflow': 'auto'}),
                        dbc.InputGroup([
                            dbc.Label("Time Value (s):", className="mr-2"),
                            dbc.Input(id='time-value-input', type='number', min=0, step=0.1, value=1),
                            dbc.Button("Confirm", n_clicks=1, id='confirm-button', color="primary", className="ml-2"),
                        ], style={'width': '400px', 'align': 'center'})
                    ],
                    align="center",
                    style={'paddingLeft': '200px'}
                ),
                dbc.Col(dcc.Graph(id='spike-frequency-heatmap', style={'resize': 'both', 'overflow': 'auto'}), align="center"),
            ]),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='average-spiking-rate-plot'), style={'resize': 'both', 'overflow': 'auto'}),
        ]),
    ], style={'margin': '30px'})

def update_channel_plot(data_processor, channel_info, value, plot_type):
    channel_idx = np.where(channel_info == value)[0][0]
    if value is not None:
        if plot_type == 'initial':
            return plot_signal(data_processor.initial_signal[channel_idx, :])
        elif plot_type == 'raster':
            return plot_single_channel_raster(data_processor.raster, channel_idx)
    return go.Figure()

def update_raster_plot(data_processor):
    return plot_raster(data_processor.raster)

def update_spike_frequency_heatmap(data_processor):
    aggregated_spikes = data_processor.aggregate_raster_spike_counts(total=True)
    return plot_spike_frequency_heatmap(aggregated_spikes, data_processor.channel_info)

def update_spike_activity_heatmap(data_processor, selected_channel, n_clicks, time_value=1):
    if selected_channel is not None and n_clicks is not None and time_value is not None:
        aggregated_spikes = data_processor.aggregate_raster_spike_counts(time_value=float(time_value), total=False)
        return plot_spike_activity_heatmap(aggregated_spikes)
    return go.Figure()

def update_average_spiking_rate_plot(data_processor):
    aggregated_spikes = data_processor.aggregate_raster_spike_counts(total=False)
    return plot_average_spiking_rate(np.sum(aggregated_spikes, axis=0))

def start_dash(data_processor: DataProcessor, channel_info):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = create_app_layout(channel_info)
    
    @callback(
        Output('channel-plot', 'figure'),
        Input('channel-dropdown', 'value'),
        Input('plot-type-selector', 'value')
    )
    def update_channel_plot_callback(value, plot_type):
        return update_channel_plot(data_processor, channel_info, value, plot_type)
   
    @callback(
        Output('raster-plot', 'figure'),
        Input('channel-dropdown', 'value')
    )
    def update_raster_plot_callback(selected_channel):
        return update_raster_plot(data_processor)
    
    @callback(
        Output('spike-frequency-heatmap', 'figure'),
        Input('channel-dropdown', 'value')
    )
    def update_spike_frequency_heatmap_callback(selected_channel):
        return update_spike_frequency_heatmap(data_processor)
    
    @callback(
        Output('spike-activity-heatmap', 'figure'),
        Input('channel-dropdown', 'value'),
        Input('confirm-button', 'n_clicks'),
        State('time-value-input', 'value')
    )
    def update_spike_activity_heatmap_callback(selected_channel, n_clicks, time_value=1):
        return update_spike_activity_heatmap(data_processor, selected_channel, n_clicks, time_value)
    
    @callback(
        Output('average-spiking-rate-plot', 'figure'),
        Input('channel-dropdown', 'value')
    )
    def update_average_spiking_rate_plot_callback(selected_channel):
        return update_average_spiking_rate_plot(data_processor)
    
    app.run_server(debug=True)

