#!/bin/bash

# Install required Python packages
pip install -r requirements.txt

# Clone the swisseph repository
git clone --depth 1 https://github.com/aloistr/swisseph.git /tmp/swisseph

# Create the directory for ephemeris data
sudo mkdir -p /usr/share/swisseph/ephe

# Copy the ephemeris files to the new directory
sudo cp -r /tmp/swisseph/ephe/* /usr/share/swisseph/ephe/

# Delete the temporary folder
rm -rf /tmp/swisseph

#====================== TERMINAL FUNCTIONS FOR EASE OF USE =====================
# RUN THESE IN TERMINAL (DOES NOT WORK IN VSCODE)
# chmod +x setup.sh
# sudo ./setup.sh

#CHECK PORT:     lsof -i :5000
#KILL PORT:      kill -9 <pid>

#IF YOU NEED A VIRTUAL ENVIRONMENT: python -m venv venv  
#BYPASS ERROR FOR .\venv\Scripts\activate
#Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process 


