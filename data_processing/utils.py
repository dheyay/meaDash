import json
import numpy as np
import pandas as pd
import scipy.io as sios

def load_data_from_mat(file_path):
    data = sios.loadmat(file_path)
    return data['filteredSignal'], data['spiketimestamps']

# TODO: Add information about the mapping
def load_node_mappings():
    with open(r"config/electrode_mapping.json", 'r') as f:
        data = json.load(f)
    return data['amplifier_channel_map']

def load_channel_info_from_json():
    with open(r"config/channel_info.json", 'r') as file:
        data = json.load(file)
        channel_info = np.array(data)
    return channel_info

# If user want's to generate a custom channel info array
def create_channel_info(nodes_dict, num_channels=60):
    channel_info = np.zeros(num_channels, dtype=int)
    for node, values in nodes_dict.items():
        intan_channel, mea_square = values
        try:
            channel_info[intan_channel] = mea_square
        except ValueError:
             # Set to 0 for invalid channels
            channel_info[intan_channel] = 0
    return channel_info

# If custom mapping needs to be generated from amplifier channel data
def generate_amplifier_mapping(amplifier_channel_data):
    mapping = {}
    for i, channel_info in enumerate(amplifier_channel_data):
        custom_channel_name = int(channel_info['custom_channel_name'])
        mapping[custom_channel_name] = i
    return mapping

def make_grid_layout(grid_array):
    layout = np.full((8, 8), np.nan)
    idx = 0
    for col in range(1, 7):
        layout[0, col] = grid_array[idx]
        idx += 1
    for col in range(0, 8):
        layout[1, col] = grid_array[idx]
        idx += 1
    for row in range(2, 7):
        for col in range(0, 8):
            layout[row, col] = grid_array[idx]
            idx += 1
    for col in range(1, 7):
        layout[7, col] = grid_array[idx]
        idx += 1
    return layout

#TODO: Update how the mapping is used (allow mapping to be in seperate config file)
#TODO: Channel info can be custom, so can the mapping
# Custom mapping is hard since we need amplifier data to get correct channel map, adding a mapping on top would be ok
def convert_to_60MEA_mapping(initial_signal, channel_info):
    """
    Convert the initial signal data to match the 60MEA layout based on the channel information.

    Args:
        initial_signal (numpy.ndarray): The initial signal data with shape (N, M), where N is the number of channels and M is the number of samples.
        channel_info (numpy.ndarray): The channel information array with shape (N,) indicating the mapping of each channel.

    Returns:
        numpy.ndarray: The rearranged data with shape (60, M) that matches the 60MEA layout.

    """
    mapping = load_node_mappings()
    rearranged_data = np.zeros((60, initial_signal.shape[1]))
    channel_info = np.where(channel_info == 0, np.nan, channel_info)
    channel_MEA_map = channel_info.copy()
    for i in range(len(channel_info)):
        try:
            channel_MEA_map[i] = mapping[str(int(channel_info[i]))]
        except:
            channel_MEA_map[i] = np.nan

    # rearrange data to match 60MEA layout
    for i, channel in enumerate(channel_MEA_map):
        try:
            if not np.isnan(channel):
                rearranged_data[i] = initial_signal[int(channel)]
        except IndexError:
            pass
    return rearranged_data

