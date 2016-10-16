#!/bin/bash
BASE_DIR=`dirname "$(readlink -f "$0")"`
cd "$BASE_DIR"

source venv/bin/activate
python ./matterbot-kuchnia.py

cd "$OLDPWD"
