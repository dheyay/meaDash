from data_processing.data_processor import DataProcessor
from app.callbacks import register_callbacks
from app import server, layouts

def start_dash(data_processor: DataProcessor, channel_info, debug=False):
    server.app.layout = layouts.create_layout(data_processor, channel_info)
    register_callbacks(server, data_processor, channel_info)
    server.app.run_server(debug=debug)