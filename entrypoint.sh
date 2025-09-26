#!/bin/bash
set -e

# Start Xvfb
Xvfb :99 -screen 0 1280x1024x24 &
XVFB_PID=$!
echo "Xvfb started with PID $XVFB_PID"

# Start openbox
openbox &
OPENBOX_PID=$!
echo "Openbox started with PID $OPENBOX_PID"

# Define cleanup function
cleanup() {
    echo "Stopping openbox and Xvfb..."
    kill $OPENBOX_PID 2>/dev/null || true
    kill $XVFB_PID 2>/dev/null || true
    exit
}

# Trap exit signals
trap cleanup SIGINT SIGTERM EXIT

# Start Flask
python main.py
