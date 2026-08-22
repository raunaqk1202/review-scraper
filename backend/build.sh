#!/usr/bin/env bash
set -e

# Install main requirements (app-store-scraper excluded due to requests==2.23.0 conflict)
pip install -r requirements.txt

# Install app-store-scraper without its dependencies (it pins requests==2.23.0
# which conflicts with our newer requests version; the scraper works fine without it)
pip install app-store-scraper==0.3.5 --no-deps
