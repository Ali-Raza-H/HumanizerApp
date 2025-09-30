#!/usr/bin/env bash
set -o errexit

# Install ncurses for tput (if using colors in scripts)
apt-get update
apt-get install -y ncurses-bin

# Install Java (needed for language_tool_python)
apt-get install -y openjdk-17-jre-headless

# Install Python dependencies
pip install -r requirements.txt
