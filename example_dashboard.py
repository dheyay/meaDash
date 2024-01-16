from plots.plotting import *
from data_processing.utils import load_data_from_mat, convert_to_60MEA_mapping
from data_processing.data_processor import DataProcessor
from data_processing.utils import load_channel_info_from_json
import numpy as np

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import scipy.io as sio

from app.index import start_dash

# Global data dictionary to store data that needs to be shared between functions
# Custom channel_info can be provided
global_data = {'initial_signal': None, 'spiketimestamps':None, 'sampling_rate': 30000, 'channel_info': load_channel_info_from_json()}
processor = None

def get_data_file():
  root = tk.Tk()
  root.withdraw()
  file_path = filedialog.askopenfilename(title='Select a file', filetypes=[('MAT files', '*.mat')])
  if file_path:
    data = load_data_from_mat(file_path)
    if data is not None:
      global_data['initial_signal'], global_data['spiketimestamps'] = data
      # Prompt the user to enter the sampling rate in a visual window
      sampling_rate = simpledialog.askinteger("Sampling Rate", "Enter the sampling rate (Hz):")
      root.destroy()
      if sampling_rate is not None:
        global_data['sampling_rate'] = sampling_rate
        return True
  root.destroy()
  return False
  
  

def main():
    isLoaded = get_data_file()
    if isLoaded:
        data_processor = DataProcessor(global_data['initial_signal'], global_data['spiketimestamps'], 
                                       global_data['sampling_rate'], global_data['channel_info'])
        start_dash(data_processor, global_data['channel_info'])
    else:
        exit()

if __name__ == '__main__':
   main()