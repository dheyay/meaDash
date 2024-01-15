import numpy as np
from utils import make_grid_layout
import sciplotlib.style as splstyle
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_single_channel_raster(boolean_signal, channel_idx, title="Channel Raster Plot", xlabel="Time"):
    num_time_points = boolean_signal.shape[1]
    spike_times = np.where(boolean_signal[channel_idx])[0]
    scatter_trace = go.Scatter(
        x=spike_times,
        y=[0] * len(spike_times),
        mode='markers',
        marker=dict(symbol='line-ns-open', size=100),
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(title=xlabel, range=[0, num_time_points]),
        yaxis=dict(visible=False),
    )
    fig = go.Figure(data=[scatter_trace], layout=layout)
    return fig

def plot_raster(boolean_signal, title="Channel Raster Plot", xlabel="Time", ylabel="Channel"):
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
        height=750
    )
    return fig

def plot_signal(signal, title='Signal', xlabel='Time', ylabel='Amplitude'):
    fig = go.Figure(data=go.Scatter(y=signal))
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    return fig

def plot_spike_frequency_heatmap(aggregated_spikes, channel_info, title='Total Spike Frequency', vmin=1, text_color='white', text_size=8):
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

# Plot correlation matrix 
def plot_correlation_matrix(electrode_correlation_matrix):
    if electrode_correlation_matrix is not None:
        with plt.style.context(splstyle.get_style('nature-reviews')):
            fig, ax = plt.subplots()
            im = ax.imshow(electrode_correlation_matrix, vmin=0, vmax=1)
            ax.set_title('Correlation matrix')
            cbar = fig.colorbar(im)
        return fig
    
def plot_average_spiking_rate(signal):
    """
    Plots the average spiking rate of a signal using Plotly.
    
    Parameters:
    signal (numpy.ndarray): The input signal.
    sampling_rate (float): The sampling rate of the signal.
    """
    fig = go.Figure(data=go.Scatter(x=np.arange(len(signal)), y=signal))
    fig.update_layout(title='Average Spiking Rate',
                      xaxis_title='Time (s)',
                      yaxis_title='Spikes',
                      showlegend=False)
    return fig

def plot_firing_rate(time_vector, firing_rate):
    fig = go.Figure(data=go.Scatter(x=time_vector, y=firing_rate))
    fig.update_layout(
        title='Aggregate Firing Rate',
        xaxis_title='Time (s)',
        yaxis_title='Firing Rate (spikes/second)',
        showlegend=False
    )
    return fig