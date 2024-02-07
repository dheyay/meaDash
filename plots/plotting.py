import numpy as np
from data_processing.utils import make_grid_layout
import sciplotlib.style as splstyle
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_single_channel_raster(boolean_signal, channel_idx, time_vector, title="Channel Raster Plot", xlabel="Time"):
    """
    Plots a raster plot for a single channel.

    Parameters:
    boolean_signal (numpy.ndarray): The boolean signal indicating spike activity.
    channel_idx (int): The index of the channel to plot.
    title (str, optional): The title of the plot. Defaults to "Channel Raster Plot".
    xlabel (str, optional): The label for the x-axis. Defaults to "Time".

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    num_time_points = boolean_signal.shape[1]
    spike_times = np.where(boolean_signal[channel_idx])[0]
    spike_time_secs = time_vector[spike_times]
    scatter_trace = go.Scatter(
        x=spike_time_secs,
        y=[0] * len(spike_times),
        mode='markers',
        marker=dict(symbol='line-ns-open', size=100),
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(title=xlabel, range=[time_vector[0], time_vector[-1]]),
        yaxis=dict(visible=False),
    )
    fig = go.Figure(data=[scatter_trace], layout=layout)
    return fig

def plot_raster(boolean_signal, title="Channel Raster Plot", xlabel="Time", ylabel="Channel"):
    """
    Plots a raster plot for multiple channels.

    Parameters:
    boolean_signal (numpy.ndarray): The boolean signal indicating spike activity.
    title (str, optional): The title of the plot. Defaults to "Channel Raster Plot".
    xlabel (str, optional): The label for the x-axis. Defaults to "Time".
    ylabel (str, optional): The label for the y-axis. Defaults to "Channel".

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    num_channels, num_time_points = boolean_signal.shape
    fig = go.Figure()
    
    for channel_idx in range(num_channels):
        spike_times = np.where(boolean_signal[channel_idx])[0]
        fig.add_trace(go.Scatter(x=spike_times, y=[channel_idx]*len(spike_times), mode='markers', marker=dict(symbol='line-ns-open', size=5)))

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis=dict(range=[-0.5, num_channels - 0.5], tickvals=list(range(num_channels))),
        xaxis=dict(range=[0, num_time_points]),
        height=1000
    )
    return fig

def plot_signal(signal, time_vector, title='Signal', xlabel='Time', ylabel='Amplitude'):
    """
    Plots a signal.

    Parameters:
    signal (numpy.ndarray): The input signal.
    title (str, optional): The title of the plot. Defaults to "Signal".
    xlabel (str, optional): The label for the x-axis. Defaults to "Time".
    ylabel (str, optional): The label for the y-axis. Defaults to "Amplitude".

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    fig = go.Figure(data=go.Scatter(x=time_vector, y=signal))
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    return fig

def plot_spike_frequency_heatmap(aggregated_spikes, channel_info, title='Total Spike Frequency', vmin=1, text_color='white', text_size=8):
    """
    Plots a heatmap of the spike frequency.

    Parameters:
    aggregated_spikes (numpy.ndarray): The aggregated spike data.
    channel_info (numpy.ndarray): The channel information.
    title (str, optional): The title of the plot. Defaults to "Total Spike Frequency".
    vmin (int, optional): The minimum value for the color scale. Defaults to 1.
    text_color (str, optional): The color of the text annotations. Defaults to "white".
    text_size (int, optional): The size of the text annotations. Defaults to 8.

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    layout = make_grid_layout(aggregated_spikes)
    vmax = np.max(aggregated_spikes)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=layout,
        zmin=vmin,
        zmax=vmax,
        colorscale='Viridis'
    ))
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=500,
        width=500
    )
    channel_layout = make_grid_layout(channel_info)
    for i in range(channel_layout.shape[0]):
        for j in range(channel_layout.shape[1]):
            if not np.isnan(channel_layout[i, j]):
                fig.add_annotation(
                    x=j,
                    y=i,
                    text=str(int(channel_layout[i, j])),
                    showarrow=False,
                    font=dict(color=text_color, size=text_size)
                )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    return fig


def plot_spike_activity_heatmap(aggregated_spikes, title="Spike Activity Over Time"):
    """
    Plots a heatmap of the spike activity over time.

    Parameters:
    aggregated_spikes (numpy.ndarray): The aggregated spike data.
    title (str, optional): The title of the plot. Defaults to "Spike Activity Over Time".

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    initial_layout = make_grid_layout(aggregated_spikes[:, 0])
    
    fig = go.Figure(
        data=go.Heatmap(
            zmin=np.min(aggregated_spikes),
            zmax=np.max(aggregated_spikes),
            z=initial_layout,
            colorscale='Viridis'
        ),
        layout=go.Layout(
            title=title,
            updatemenus=[{"type": "buttons", "buttons": [{"label": "Play",
                                                          "method": "animate",
                                                          "args": [None]}]}],
            height=500,
            width=500
        )
    )
    
    frames = [go.Frame(data=[go.Heatmap(z=make_grid_layout(aggregated_spikes[:, i]))], 
                    name=str(i)) for i in range(aggregated_spikes.shape[1])]
    fig.frames = frames

    sliders = [{
        'steps': [{'method': 'animate', 'args': [[f.name], 
                 {'mode': 'immediate', 'frame': {'duration': 1, 'redraw': True}}],
                  'label': str(i)} for i, f in enumerate(fig.frames)],
        'transition': {'duration': 1},
        'x': 0.1, 'len': 0.8
    }]

    fig.update_layout(sliders=sliders)
    return fig

def plot_correlation_matrix(electrode_correlation_matrix):
    """
    Plots the correlation matrix.

    Parameters:
    electrode_correlation_matrix (numpy.ndarray): The correlation matrix.

    Returns:
    matplotlib.figure.Figure: The generated matplotlib figure.
    """
    if electrode_correlation_matrix is not None:
        with plt.style.context(splstyle.get_style('nature-reviews')):
            fig, ax = plt.subplots()
            im = ax.imshow(electrode_correlation_matrix, vmin=0, vmax=1)
            ax.set_title('Correlation matrix')
            cbar = fig.colorbar(im)
        return fig
    
def plot_average_spiking_rate(spikingRate, title='Average Spiking Rate'):
    """
    Plots the average spiking rate of a signal.

    Parameters:
    signal (numpy.ndarray): The input signal.
    title (str, optional): The title of the plot. Defaults to "Average Spiking Rate".

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    fig = go.Figure(data=go.Scatter(x=np.arange(len(spikingRate)), y=spikingRate))
    fig.update_layout(title=title,
                      xaxis_title='Time (s)',
                      yaxis_title='Spikes',
                      showlegend=False)
    return fig

def plot_firing_rate(firing_rate, time_vector, title='Aggregate Firing Rate'):
    """
    Plots the firing rate over time.

    Parameters:
    time_vector (numpy.ndarray): The time vector.
    firing_rate (numpy.ndarray): The firing rate data.
    title (str, optional): The title of the plot. Defaults to "Aggregate Firing Rate".

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    fig = go.Figure(data=go.Scatter(x=time_vector, y=firing_rate))
    fig.update_layout(
        title=title,
        xaxis_title='Time (s)',
        yaxis_title='Firing Rate (spikes/second)',
        showlegend=False
    )
    return fig

def plot_psd(frequencies, pxx, center_frequency):
    """
    Plots the power spectral density.

    Parameters:
    frequencies (numpy.ndarray): The frequency values.
    pxx (numpy.ndarray): The power spectral density values.
    center_frequency (float): The center frequency.

    Returns:
    plotly.graph_objects.Figure: The generated plotly figure.
    """
    max_pxx = np.max(pxx)
    # Create traces
    trace0 = go.Scatter(
        x = frequencies,
        y = 10 * np.log10(pxx),
        mode = 'lines',
        name = 'PSD',
        line = dict(width=1.8)
    )

    trace1 = go.Scatter(
        x = [center_frequency],
        y = [10 * np.log10(max_pxx)],
        mode = 'markers',
        name = 'Peak',
        marker = dict(color='red', size=10)
    )

    trace2 = go.Scatter(
        x = [center_frequency, center_frequency],
        y = [14, 10 * np.log10(max_pxx)],
        mode = 'lines',
        name = 'Line',
        line = dict(color='black', width=2, dash='dash')
    )

    layout = go.Layout(
        title='Welch Power Spectral Density for MEA',
        xaxis=dict(
            title='Frequency (Hz)',
            range=[0, 2],
            dtick=0.2
        ),
        yaxis=dict(
            title='Power/Frequency (dB/Hz)',
            range=[14, 36],
            dtick=2
        ),
        showlegend=False
    )

    fig = go.Figure(data=[trace0, trace1, trace2], layout=layout)
    return fig