#!/bin/bash
export FLASK_APP=./src/main.py
# source $(pipenv --venv)/bin/activate
py -m flask run -h 0.0.0.0