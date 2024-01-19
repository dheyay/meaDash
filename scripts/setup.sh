#!/bin/bash

# Navigate to the project directory (modify as needed)

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Setup complete. Run 'source run.sh' to start the dashboard."

