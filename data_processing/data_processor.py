# standard imports
import os
from data_processing.utils import convert_to_60MEA_mapping

# third party imports
import numpy as np
import scipy.io as sios
import scipy.signal as ssignal

class DataProcessor:
    """
    A class for processing data from a 60MEA mapping.

    Args:
        initial_signal (numpy.ndarray): The initial signal.
        spike_timestamps (list): The spike timestamps.
        sampling_rate (float): The sampling rate of the signal.
        channel_info (dict): Information about the channels.

    Attributes:
        initial_signal (numpy.ndarray): The initial signal.
        spike_timestamps (list): The spike timestamps.
        sampling_rate (float): The sampling rate of the signal.
        channel_info (dict): Information about the channels.
        raster (numpy.ndarray): The raster representation of the spike timestamps.

    Methods:
        create_raster: Creates a raster representation of the spike timestamps.
        get_spikes_by_timestamp_per_channel: Retrieves spike traces within a given time window.
        downsample_raster_to_binary_presence: Downsamples the raster to binary presence.
        aggregate_raster_spike_counts: Aggregates spike counts in fixed time intervals.
        get_active_channels: Retrieves active channels based on spike counts.
        convolve_signal: Convolves the signal with a given kernel.
        estimate_power_spectral_density: Estimates the power spectral density of the signal.

    """

    def __init__(self, initial_signal, spike_timestamps, sampling_rate, channel_info):
        # TODO: Convert the initial signal and spike_timestamps to a 60MEA mapping
        self.initial_signal = convert_to_60MEA_mapping(initial_signal, channel_info)
        self.spike_timestamps = convert_to_60MEA_mapping(spike_timestamps, channel_info)
        self.sampling_rate = sampling_rate
        self.channel_info = channel_info
        self.raster = self.create_raster()

    def create_raster(self):
        """
        Creates a raster representation of the spike timestamps.

        Returns:
            numpy.ndarray: The raster representation of the spike timestamps.

        """
        raster = np.zeros_like(self.initial_signal)
        for channel in range(len(self.spike_timestamps)):
            for ts in self.spike_timestamps[channel]:
                raster[channel, int(ts)] = 1
        return raster

    def get_spikes_by_timestamp_per_channel(self, left_bound=0.2, right_bound=0.3):
        """
        Retrieves spike traces within a given time window.

        Args:
            left_bound (float): The left bound of the time window in seconds. Default is 0.2.
            right_bound (float): The right bound of the time window in seconds. Default is 0.3.

        Returns:
            dict: A dictionary containing spike traces per channel.

        """
        l = -int(left_bound * self.sampling_rate)
        r = int(right_bound * self.sampling_rate)
        spike_traces = {}
        for channel in range(len(self.spike_timestamps)):
            spike_traces[channel] = {}
            for ts in self.spike_timestamps[channel]:
                if ts != 0:
                    spike_trace = self.initial_signal[channel, ts + l:ts + r]
                    spike_traces[channel][ts] = spike_trace
        return spike_traces

    def downsample_raster_to_binary_presence(self, time_per_bucket):
        """
        Downsamples the raster to binary presence.

        Args:
            time_per_bucket (float): The time duration per bucket in seconds.

        Returns:
            numpy.ndarray: The downsampled binary presence matrix.

        """
        samples_per_bucket = int(self.sampling_rate * time_per_bucket)
        num_buckets = self.raster.shape[1] // samples_per_bucket
        binary_presence = np.zeros((self.raster.shape[0], num_buckets))
        for channel in range(self.raster.shape[0]):
            for bucket in range(num_buckets):
                start_index = bucket * samples_per_bucket
                end_index = start_index + samples_per_bucket
                binary_presence[channel, bucket] = np.any(self.raster[channel, start_index:end_index])
        return binary_presence.astype(int)

    def aggregate_raster_spike_counts(self, time_value=1, total=False):
        """
        Aggregates spike counts in fixed time intervals.

        Args:
            time_value (float): The time value for each interval in seconds. Default is 1.
            total (bool): Whether to compute the total spike count. Default is False.

        Returns:
            numpy.ndarray: The aggregated spike counts.

        Raises:
            AssertionError: If the time value exceeds the signal duration in seconds.

        """
        assert time_value <= self.raster.shape[1] / self.sampling_rate, "Time value exceeds signal duration in seconds"
        if total:
            return np.sum(self.raster, axis=1)
        bucket_size = int(self.sampling_rate * time_value)
        num_buckets = self.raster.shape[1] // bucket_size
        aggregated_counts = np.zeros((self.raster.shape[0], num_buckets))
        for bucket in range(num_buckets):
            start = bucket * bucket_size
            end = start + bucket_size
            aggregated_counts[:, bucket] = np.sum(self.raster[:, start:end], axis=1)
        return aggregated_counts

    def get_active_channels(self, active_channel_threshold=5):
        """
        Retrieves active channels based on spike counts.

        Args:
            active_channel_threshold (int): The threshold for considering a channel as active. Default is 5.

        Returns:
            numpy.ndarray: The indices of the active channels.

        """
        aggregate = self.aggregate_raster_spike_counts(total=True)
        active_channels = np.array([i for i, channel in enumerate(aggregate) if np.mean(channel) >= active_channel_threshold])
        return active_channels

    def convolve_signal(self, windowsize, conv_type='boxcar'):
        """
        Convolves the signal with a given kernel.

        Args:
            windowsize (float): The size of the convolution window in seconds.
            conv_type (str): The type of convolution. Supported types are 'boxcar' and 'dual_exp'. Default is 'boxcar'.

        Returns:
            numpy.ndarray: The convolved signal.

        Raises:
            ValueError: If the convolution type is invalid.

        """
        if conv_type == 'boxcar':
            kernel = ssignal.boxcar(int(windowsize * self.sampling_rate))
        else:
            raise ValueError("Invalid convolution type. Supported types are 'boxcar' and 'dual_exp'.")

        convolved_signal = np.zeros_like(self.raster)
        for i in range(self.raster.shape[0]):
            f = self.raster[i]
            fw = ssignal.convolve(f, kernel, mode='same')
            convolved_signal[i] = fw
        return convolved_signal

    def estimate_power_spectral_density(self, conv_sig_sum, window_length=None, noverlap=None, nfft=None, kernel=None):
        """
        Estimates the power spectral density of a signal using Welch's method.

        Args:
            conv_sig_sum (numpy.ndarray): The convolved signal.
            window_length (int): The length of the window for Welch's method. Default is None.
            noverlap (int): The number of overlapping samples between windows. Default is None.
            nfft (int): The number of points to compute the FFT. Default is None.
            kernel (str): The window function to use. Default is None.

        Returns:
            numpy.ndarray: The frequencies.
            numpy.ndarray: The power spectral density.
            float: The center frequency.

        """
        detrended = ssignal.detrend(conv_sig_sum, type='linear')
        if window_length is None:
            window_length = len(detrended) // 8
        if nfft is None:
            nfft = (2 ** np.ceil(np.log2(window_length))) * 2
        if noverlap is None:
            noverlap = window_length // 2
        if kernel is None:
            kernel = 'boxcar'

        frequencies, pxx = ssignal.welch(detrended, fs=self.sampling_rate, window=kernel,
                                         nperseg=window_length, noverlap=noverlap, nfft=nfft, scaling='density',
                                         axis=0, detrend=False, average='mean')

        max_index = np.argmax(pxx)
        center_frequency = frequencies[max_index]
        return frequencies, pxx, center_frequency