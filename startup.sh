#!/bin/sh

# FETCHIT startup script for the receiving screen application
# Maintainer @kevintruck

# REQUIREMENTS
# 1. AWS Credentials for stage bucket
# 2. SSH Key for github


# Check for internet connection

# If connected, get latest version
python main.py

# start app
install/./FetchItRS

##### We might need an ssh key to get this repo
##### also need a temp key for each rs
