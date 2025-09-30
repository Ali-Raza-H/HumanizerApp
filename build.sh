#!/usr/bin/env bash
set -o errexit

# Install Java (needed for language_tool_python)
apt-get update
apt-get install -y openjdk-17-jre-headless

# Install Python dependencies
pip install -r requirements.txt
