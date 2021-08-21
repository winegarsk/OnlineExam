#!/bin/bash

export FLASK_APP=./src/main.py
source $(pipenv --venv)/bin/activate

flask run -h 127.0.0.1 -p 5000