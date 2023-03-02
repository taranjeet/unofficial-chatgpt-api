#!/bin/sh

# exit on error
set -e

# create a virtual envoirment if it doesn't exist
if [ ! -d pyenv ]; then
    echo "Creating virtual environment"
    virtualenv -p $(which python3) pyenv
fi

echo "Activating virtual environment"
source pyenv/bin/activate

echo "Installing requirements"
pip install -r requirements.txt

echo "Installing playwright chromium driver"
playwright install

echo "Starting server"
python server.py