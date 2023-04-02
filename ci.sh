#!/bin/bash

# Pull the latest changes
git pull

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
