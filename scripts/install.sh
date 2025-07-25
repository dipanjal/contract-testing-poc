#!/bin/bash

pyenv install -s

DIRECTORY=".venv"

if [ -d "$DIRECTORY" ]; then
    echo "Removing existing $DIRECTORY"
    rm -rf $DIRECTORY
fi
echo "Creating new venv"
python -m venv $DIRECTORY
source $DIRECTORY/bin/activate

which python

pip install -r requirements.txt