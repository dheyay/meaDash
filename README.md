# meaDash

meaDash is a dashboard for analyzing and visualizing neural signal data obtained from a multi-electrode array (MEA). This project aims to provide a user-friendly interface for researchers and scientists to explore and gain insights from their MEA data.

(currently customized for use in Center for BioMedical Signal Processing and Computation, University of California Irvine)

## Features

- Data Visualization: meaDash offers various visualization tools to help users analyze and interpret their MEA data. These include interactive plots, heatmaps, and spike raster plots.

- Data Analysis: The dashboard provides built-in algorithms and statistical methods for analyzing MEA data. Users can perform spike sorting, calculate firing rates, and extract various features from the neural signals.

- User-Friendly Interface: meaDash is designed with a clean and intuitive interface, making it easy for users to navigate and interact with their data. The dashboard provides interactive controls and customizable settings to tailor the analysis to specific needs.

## Installation

To install meaDash, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/meaDash.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Launch the dashboard:
    ```bash
    python example_dashboard.py
    ```

### Setup and Execution Scripts

To set up a Python virtual environment and install the required dependencies, you can use the following scripts:

- `setup.sh` (for Unix-based systems) or `setup.bat` (for Windows systems): These scripts create a virtual environment and install the necessary packages using `pip`. You can modify these scripts to add any additional setup steps or customize the environment.

- `run.sh` (for Unix-based systems) or `run.bat` (for Windows systems): This script activates the virtual environment and runs the program. You can modify this script to include any additional commands or configurations required to run your program.

## Usage

### Configuration of the MEA
To use meaDash with your specific MEA setup, you need to provide the configuration details. This includes the number of channels, the sampling rate, and the electrode layout. You can modify the configuration file `config/electrode_mapping.json` to match your MEA specifications. This maps the intan mea electrode to the custom channel name as per the signal rhs file. Needs to be updated manually currently.

### Custom Channel Info
If you want to add custom channel information, such as the location or type of electrodes, you can do so by editing the `channel_info.json` file. This allows you to have a more detailed analysis and visualization of your MEA data. This channel_info file contains an array of length 60 with the 60 electrodes in order. This array can be updated as per a custom mapping.

### Running the dashboard
You will get a dialog box to locally select a ".mat" file which contains the spike detection run signal data under the variable 'filteredSignal' and the spike times under the variable 'spiketimestamps'. Then you will be prompted to enter the sampling rate for the signal in Hz.

-Spike detection algorithms and methods need to be added so a raw signal can be analyzed.-

Once the dashboard is running, you will see a link in the terminal (Ctrl + click the link) or open your web browser and navigate to `http://localhost:5000` to access meaDash. From there, you can explore the visualizations, and perform data analysis tasks.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or suggestions regarding meaDash, please feel free to contact us: [Shravan Thaploo](mailto:sthaploo@uci.edu) and [Dheyay Desai](mailto:desaidn@uci.edu).

