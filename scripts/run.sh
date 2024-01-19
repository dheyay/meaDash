#!/bin/bash

# Set the path to your project directory
PROJECT_DIR=""

# Navigate to the project directory
cd "$PROJECT_DIR"

# Check if the virtual environment directory exists

# Activate the virtual environment
source venv/bin/activate

# Run the main Python program
python example_dashboard.py

# Deactivate the virtual environment
deactivate

