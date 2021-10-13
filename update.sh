#!/bin/bash
set -e

date

# Install dependencies
python3 -m pip install -r requirements.txt

git checkout gh-pages
git pull origin gh-pages
