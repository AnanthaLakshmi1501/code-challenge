@echo off
setlocal enabledelayedexpansion


echo "_______________________________________________________________________________"
echo "Creating & Activating Virtual Environment..."
pip install virtualenv
:: Create a virtual environment
call virtualenv venv

:: Activate the virtual environment
call venv\Scripts\activate

echo "_______________________________________________________________________________"
echo "Installing Requirements..."
:: Install requirements using pip
call pip install -r requirements.txt

cd src
call python manage.py makemigrations
call python manage.py migrate

cd ..
echo "_______________________________________________________________________________"
echo "Ingesting Data..."
:: Run the ingest.py script (change 'ingest.py' to your script name if different)
call python data_ingestion.py

cd src
echo "_______________________________________________________________________________"

set DJANGO_SETTINGS_MODULE=weatherapp.settings
echo "Running Tests..."

call pytest -v
:: Start the Django development server
echo "_______________________________________________________________________________"
echo "Running Server..."
call python manage.py runserver

endlocal
