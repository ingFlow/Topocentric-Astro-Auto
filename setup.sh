#!/bin/bash

# Install required Python packages
pip install julian pyswisseph flask timezonefinder kerykeion pandas

# Clone the swisseph repository
git clone --depth 1 https://github.com/aloistr/swisseph.git /tmp/swisseph

# Create the directory for ephemeris data
sudo mkdir -p /usr/share/swisseph/ephe

# Copy the ephemeris files to the new directory
sudo cp -r /tmp/swisseph/ephe/* /usr/share/swisseph/ephe/

# Delete the temporary folder
rm -rf /tmp/swisseph

#check port is lsof -i :5000
#kill port is kill -9 <pid>

# RUN THESE IN TERMINAL
# chmod +x setup.sh
# sudo ./setup.sh
