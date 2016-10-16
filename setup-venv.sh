#!/bin/bash
virtualenv venv
source venv/bin/activate
STATIC_DEPS=true pip install lxml
pip install -r requirements.txt
