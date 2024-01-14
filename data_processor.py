# standard imports
import os
from utils import convert_to_60MEA_mapping

# third party imports
import numpy as np
import scipy.io as sios

class DataProcessor:
    def __init__(self, initial_signal, spike_timestamps, sampling_rate, channel_info):
        # TODO: Conver the intial signal and spike_timestamps to a 60MEA mapping
        self.initial_signal = convert_to_60MEA_mapping(initial_signal, channel_info)
        self.spike_timestamps = convert_to_60MEA_mapping(spike_timestamps, channel_info)
        self.sampling_rate = sampling_rate
        self.channel_info = channel_info
        self.raster = self.create_raster()

    def create_raster(self):
        raster = np.zeros_like(self.initial_signal)
        for channel in range(len(self.spike_timestamps)):
            for ts in self.spike_timestamps[channel]:
                raster[channel, int(ts)] = 1
        return raster

    def get_spikes_by_timestamp_per_channel(self, left_bound=0.2, right_bound=0.3):
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
        samples_per_bucket = int(self.sampling_rate * time_per_bucket)
        num_buckets = self.raster.shape[1] // samples_per_bucket
        binary_presence = np.zeros((self.raster.shape[0], num_buckets))
        for channel in range(self.raster.shape[0]):
            for bucket in range(num_buckets):
                start_index = bucket * samples_per_bucket
                end_index = start_index + samples_per_bucket
                binary_presence[channel, bucket] = np.any(self.raster[channel, start_index:end_index])
        return binary_presence.astype(int)

    def aggregate_raster_spike_counts(self, time_value = 1, total=False):
        assert time_value <= self.raster.shape[1] / self.sampling_rate, "Time value exceeds signal duration in seconds"
        if total == True:
            return np.sum(self.raster, axis=1)
        bucket_size = int(self.sampling_rate * time_value)
        num_buckets = self.raster.shape[1] // bucket_size
        aggregated_counts = np.zeros((self.raster.shape[0], num_buckets))
        for bucket in range(num_buckets):
            start = bucket * bucket_size
            end = start + bucket_size
            aggregated_counts[:, bucket] = np.sum(self.raster[:, start:end], axis=1)
        return aggregated_counts


    #TODO: Implement this
    def calculate_final_spiking_rate(self, time_value, active_channel_threshold=5):
        pass

    #TODO: Implement convolution function for the channels (boxcar, gaussian, double exponential)