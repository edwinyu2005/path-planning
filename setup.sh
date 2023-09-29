#!/bin/bash

set -e

venv='.venv'
if [ ! -d $venv ]; then
    echo "Creating a new virtualenv"
    virtualenv -p python3 .venv
fi

source .venv/bin/activate

# Upgrade pip and install flake8
pip install --upgrade pip
pip install flake8

# Install other dependencies from requirements.txt, if it exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "OK! good to go!"
echo "Just run the following:"
echo "source .venv/bin/activate"
