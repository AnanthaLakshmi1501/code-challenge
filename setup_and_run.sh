#!/bin/bash

VENV_SCRIPT="venv/bin/activate"
PYTHON_VAR="python3"

echo "_______________________________________________________________________________"
echo "Creating & Activating Virtual Environment..."
pip install virtualenv
# Create a virtual environment
$PYTHON_VAR -m venv venv

# Activate the virtual environment
source $VENV_SCRIPT

echo "_______________________________________________________________________________"
echo "Installing Requirements..."
# Install requirements using pip
pip install -r requirements.txt

cd src
$PYTHON_VAR manage.py makemigrations
$PYTHON_VAR manage.py migrate

cd ..
echo "_______________________________________________________________________________"
echo "Ingesting Data..."
# Run the ingest.py script (change 'ingest.py' to your script name if different)
$PYTHON_VAR data_ingestion.py

cd src
echo "_______________________________________________________________________________"

export DJANGO_SETTINGS_MODULE=weatherapp.settings
echo "Running Tests..."


pytest -v
# Start the Django development server
echo "_______________________________________________________________________________"
echo "Running Server..."
$PYTHON_VAR manage.py runserver

