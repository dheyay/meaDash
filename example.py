from plotting import *
from utils import load_data_from_mat, convert_to_60MEA_mapping
from data_processor import DataProcessor
import numpy as np

import tkinter as tk
from tkinter import filedialog, messagebox
import scipy.io as sio

from index import start_dash

# from board import start_dash
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

def main():
    isLoaded = get_data_file()
    if isLoaded:
        data_processor = DataProcessor(global_data['initial_signal'], global_data['spiketimestamps'], sampling_rate, channel_info)
        start_dash(data_processor, channel_info)
    else:
        exit()

if __name__ == '__main__':
   main()