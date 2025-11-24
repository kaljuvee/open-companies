#!/bin/bash

# Activate virtual environment
source /home/ubuntu/open-companies/venv/bin/activate

# Set environment variables from .env file
# Copy .env.sample to .env and fill in your credentials
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run Streamlit
cd /home/ubuntu/open-companies
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
