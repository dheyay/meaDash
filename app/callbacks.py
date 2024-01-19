from dash import dcc, html, callback, Output, Input, State
from app import server, layouts
from plots.plotting import *
from data_processing.data_processor import DataProcessor


def update_channel_plot(data_processor, channel_info, value, plot_type):
    channel_idx = value
    if value is not None:
        if plot_type == 'initial':
            return plot_signal(data_processor.initial_signal[channel_idx, :])
        elif plot_type == 'raster':
            return plot_single_channel_raster(data_processor.raster, channel_idx)
    return go.Figure()

def update_spike_frequency_heatmap(data_processor):
    aggregated_spikes = data_processor.aggregate_raster_spike_counts(total=True)
    return plot_spike_frequency_heatmap(aggregated_spikes, data_processor.channel_info)

def update_spike_activity_heatmap(data_processor, n_clicks, time_value=1):
    if n_clicks is not None and time_value is not None:
        aggregated_spikes = data_processor.aggregate_raster_spike_counts(time_value=float(time_value), total=False)
        return plot_spike_activity_heatmap(aggregated_spikes)
    return go.Figure()

def update_spiking_rate_plot(data_processor, windowsize):
    convolved_sig = data_processor.convolve_signal(windowsize, 'boxcar')
    conv_sum = np.sum(convolved_sig, axis=0)
    conv_sum_spikepersecond = conv_sum / windowsize
    sampleindices = np.arange(conv_sum.shape[0])
    timeinseconds_vec = sampleindices / data_processor.sampling_rate
    return plot_firing_rate(timeinseconds_vec, conv_sum_spikepersecond, title=r"Spiking Rate - window size: " + str(windowsize) + " s")

def update_psd_plot(data_processor, windowsize):
    convolved_sig = data_processor.convolve_signal(windowsize, 'boxcar')
    conv_sum = np.sum(convolved_sig, axis=0)
    frequencies, pxx, center_frequency = data_processor.estimate_power_spectral_density(conv_sum)
    return plot_psd(frequencies, pxx, center_frequency)

def register_callbacks(server, data_processor: DataProcessor, channel_info, debug=False):
    """
    Register callbacks for updating the app's components based on user interactions.

    Args:
        server (dash.Dash): The Dash server instance.
        data_processor (DataProcessor): An instance of the DataProcessor class.
        channel_info (dict): Information about the channels.
        debug (bool, optional): Flag to enable debug mode. Defaults to False.
    """
    @server.app.callback(
        Output('sidebar', 'children'),
        [Input('url', 'pathname')]
    )
    def update_sidebar(pathname):
        return layouts.generate_sidebar(pathname, channel_info)


    @server.app.callback(
        Output('channel-plot', 'figure'),
        Input('channel-dropdown', 'value'),
        Input('plot-type-selector', 'value')
    )
    def update_channel_plot_callback(value, plot_type):
        return update_channel_plot(data_processor, channel_info, value, plot_type)
   
    
    @server.app.callback(
        Output('spike-frequency-heatmap', 'figure'),
        Input('channel-dropdown', 'value')
    )
    def update_spike_frequency_heatmap_callback(selected_channel):
        return update_spike_frequency_heatmap(data_processor)
    
    @server.app.callback(
        Output('spike-activity-heatmap', 'figure'),
        Input('confirm-button', 'n_clicks'),
        State('time-value-input', 'value')
    )
    def update_spike_activity_heatmap_callback(n_clicks, time_value=1):
        return update_spike_activity_heatmap(data_processor,n_clicks, time_value)
    
    
    @server.app.callback(
        Output('firing-rate-plot', 'figure'),
        Input('apply-button', 'n_clicks'),
        State('window-size-input', 'value')
    )
    def update_spiking_rate_plot_callback(n_clicks, windowsize):
        return update_spiking_rate_plot(data_processor, windowsize)
    
    @server.app.callback(
        Output('power-spectral-density-plot', 'figure'),
        Input('apply-button', 'n_clicks'),
        State('window-size-input', 'value')
    )
    def update_psd_plot_callback(n_clicks, windowsize):
        return update_psd_plot(data_processor, windowsize)
    
    @server.app.callback(
        [Output(f"page-{i}-link", "active") for i in range(1, 4)],
        [Input("url", "pathname")]
    )
    def toggle_active_links(pathname):
        if pathname in ["/", "/page-1"]:
            return True, False, False
        elif pathname == "/page-2":
            return False, True, False
        elif pathname == "/page-3":
            return False, False, True
        return False, False, False
    
    @server.app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def render_page_content(pathname):
        if not pathname or pathname == '/' or pathname == '/page-1':
            return layouts.page_1_layout()
        elif pathname == '/page-2':
            return layouts.page_2_layout(data_processor)
        elif pathname == '/page-3':
            return layouts.page_3_layout(data_processor)
        return '404 Page Not Found'