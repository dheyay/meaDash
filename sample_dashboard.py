from plotting import *
from utils import load_data_from_mat, convert_to_60MEA_mapping
from data_processor import DataProcessor
import numpy as np

import tkinter as tk
from tkinter import filedialog, messagebox
import scipy.io as sio
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime
"""
Sample Data processing pipeline

1. Import data from the .mat file
2. Convert the data to a 60MEA mapping
[Allow user to specify variables such as channel info, sampling rate, etc.]
3. Create a DataProcessor object
4. Use the DataProcessor object to save the raster plot
4. (Optional) Use DataProcessor to downsample the raster plot to a binary presence array
5. (Optional) Use DataProcessor to aggregate the raster plot to a spike count array
6. Plot the raster plot 
7. Plot the binary presence array | spike firing rate as per desired time value
8. Plot heatmap of spike count array
9. Plot spike frequency heatmap
10. Plot spike frequency heatmap animation with grid layout
11. [Allow plotting of convolved signal | spike firing rates | ]
"""

sampling_rate = 30000
# channel_info = np.array(    [82, 83, 84, 85, 86, 
#                          87, 71, 72, 73, 74, 75, 76, 
#                          77, 78, 61, 62, 63, 64, 65, 
#                          66, 67, 68, 51, 52, 53, 54, 
#                          55, 56, 57, 58, 41, 42, 43, 
#                          44, 45, 46, 47, 48, 31, 32, 
#                          33, 34, 35, 36, 37, 38, 21, 
#                          22, 23, 24, 25, 26, 27, 28, 
#                             12, 13, 14, 0, 16, 17])
channel_info = np.array([  33, 22, 12, 23, 13, 
                         34, 24, 14, 0, 25, 35, 16, 
                         26, 17, 27, 36, 28, 37, 38, 
                         45, 46, 0, 0, 57, 58, 56, 
                         55, 68, 67, 78, 66, 77, 87, 
                         76, 86, 65, 75, 85, 84, 74, 
                         64, 83, 73, 82, 72, 63, 71, 
                         62, 61, 54, 53, 51, 52, 0, 
                         41, 43, 44, 31, 32, 21])

# Custom channel_info can be provided
global_data = {'initial_signal': None, 'spiketimestamps':None, 'sampling_rate': None, 'channel_info': channel_info}
processor = None

def get_data_file():
  root = tk.Tk()
  root.withdraw()
  file_path = filedialog.askopenfilename(title='Select a file', filetypes=[('MAT files', '*.mat')])
  root.destroy()
  if file_path:
    data = load_data_from_mat(file_path)
    if data is not None:
      global_data['initial_signal'], global_data['spiketimestamps'] = data
      return True

  else:
    return False

def start_dash_app(data_processor: DataProcessor):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
      html.H1("Neural Signal Analysis Dashboard [60 MEA]", style={'textAlign': 'center', 'margin': '50px'}),
      dbc.Row([
        dbc.Col(dcc.Dropdown(
          id='channel-dropdown',
          value=channel_info[0],
          options=[{'label': f'Channel {i}', 'value': i} for i in range(len(channel_info))],
          placeholder='Select a Channel'
        ), width={'size': 4, 'offset': 3}, style={'margin': '10px'}),
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
        dbc.Col(dcc.Graph(id='raster-plot')),
      ]),
      dbc.Row([
        dbc.Row([
          dbc.Col(
            [
              dcc.Graph(id='spike-activity-heatmap'),
              dbc.InputGroup([
                dbc.Label("Time Value (s):", className="mr-2"),
                dbc.Input(id='time-value-input', type='number', min=0, step=0.1, value=1),
                dbc.Button("Confirm", n_clicks=1, id='confirm-button', color="primary", className="ml-2"),
              ], style={'width': '400px', 'align': 'center'})
            ],
            align="center",
            style={'paddingLeft': '100px', 'margin': '10px'}
          ),
          dbc.Col(dcc.Graph(id='spike-frequency-heatmap'), align="center"),
        ]),
      ]),
      dbc.Row([
        dbc.Col(dcc.Graph(id='average-spiking-rate-plot')),
      ]),
    ], style={'padding': '20px'})
    
    @callback(
      Output('channel-plot', 'figure'),
      Input('channel-dropdown', 'value'),
      Input('plot-type-selector', 'value')
    )
    def update_channel_plot(value, plot_type):
      channel_idx = np.where(channel_info == value)[0][0]
      if value is not None:
         if plot_type == 'initial':
            return plot_signal(data_processor.initial_signal[channel_idx, :])
         elif plot_type == 'raster':
            return plot_single_channel_raster(data_processor.raster, channel_idx)
      return go.Figure()
   
    @callback(
      Output('raster-plot', 'figure'),
      Input('channel-dropdown', 'value')
    )
    def update_raster_plot(selected_channel):
      return plot_raster(data_processor.raster)
    
    @callback(
      Output('spike-frequency-heatmap', 'figure'),
      Input('channel-dropdown', 'value')
    )
    def update_spike_frequency_heatmap(selected_channel):
      if selected_channel is not None:
         aggregated_spikes = data_processor.aggregate_raster_spike_counts(total=True)
         return plot_spike_frequency_heatmap(aggregated_spikes, data_processor.channel_info)
      return go.Figure()
    
    @callback(
      Output('spike-activity-heatmap', 'figure'),
      Input('channel-dropdown', 'value'),
      Input('confirm-button', 'n_clicks'),
      State('time-value-input', 'value')
    )
    def update_spike_activity_heatmap(selected_channel, n_clicks, time_value=1):
      if selected_channel is not None and n_clicks is not None and time_value is not None:
         aggregated_spikes = data_processor.aggregate_raster_spike_counts(time_value=float(time_value), total=False)
         return plot_spike_activity_heatmap(aggregated_spikes)
      return go.Figure()
    
    @callback(
      Output('average-spiking-rate-plot', 'figure'),
      Input('channel-dropdown', 'value')
    )
    def update_average_spiking_rate_plot(selected_channel):
      if selected_channel is not None:
         aggregated_spikes = data_processor.aggregate_raster_spike_counts(total=False)
         return plot_average_spiking_rate(np.sum(aggregated_spikes, axis=0))
      return go.Figure()
    
    app.run_server(debug=True)

def main():
    isLoaded = get_data_file()
    if isLoaded:
        data_processor = DataProcessor(global_data['initial_signal'], global_data['spiketimestamps'], sampling_rate, channel_info)
        start_dash_app(data_processor)
    else:
        exit()

if __name__ == '__main__':
   main()