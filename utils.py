import json
import numpy as np
import pandas as pd

#TODO: Update how the mapping is used (allow mapping to be in seperate config file)
#TODO: Channel info can be custom, so can the mapping
#TODO: Mapping needs to be in the format -> row['RHS']: [row['Intan'], row['MEA Square']]
def convert_to_60MEA_mapping(self, mapping):
    custom_data = np.zeros((60, self.initial_signal.shape[1]))
    channel_info = np.where(self.channel_info == 0, np.nan, self.channel_info)
    channel_MEA_map = channel_info.copy()

    for i in range(len(channel_info)):
        try:
            channel_MEA_map[i] = mapping[channel_info[i]]
        except KeyError:
            channel_MEA_map[i] = np.nan
            print("Node missing: ", channel_info[i])

    for i, channel in enumerate(channel_MEA_map):
        try:
            if not np.isnan(channel):
                custom_data[i] = self.initial_signal[int(channel)]
        except IndexError:
            print("Missing Node")
    return custom_data

# TODO: Add information about the mapping
# The mapping is a dictionary that maps the custom channel name to the index of the amplifier channel
# The mapping is generated from the amplifier channel data in an INTAN rhs file
def load_node_mappings():
    with open(r"config/electrode_mapping.json", 'r') as f:
        data = json.load(f)
    return {row['RHS']: [row['Intan'], row['MEA Square']] for row in data}

def create_channel_info(nodes_dict, num_channels=60):
    channel_info = np.zeros(num_channels, dtype=int)
    for node, values in nodes_dict.items():
        intan_channel, mea_square = values
        try:
            channel_info[intan_channel] = mea_square
        except ValueError:
            channel_info[intan_channel] = 0  # Set to 0 for invalid channels
    return channel_info

def generate_mapping(amplifier_channels):
    mapping = {}
    for i, channel_info in enumerate(amplifier_channels):
        custom_channel_name = int(channel_info['custom_channel_name'])
        mapping[custom_channel_name] = i
    return mapping

# # Example usage:
# nodes_dict = load_node_mappings()
# channel_info = create_channel_info(nodes_dict)
# # Assuming 'result' is a predefined variable containing amplifier channel data.
# mapping = generate_mapping(result['amplifier_channels'])

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
