#!/bin/bash

virtualenv -p $(which python3) venv
. ./venv/bin/activate
pip install -e .
