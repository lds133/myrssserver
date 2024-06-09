#!/bin/bash

# sudo apt install python3.10-venv

rm -rf .venv

python3 -m venv .venv


.venv/bin/pip3 install -r requirements.txt
