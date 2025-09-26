#!/bin/bash
set -e

Xvfb :99 -screen 0 1280x1024x24 &
XVFB_PID=$!
echo "Xvfb started with PID $XVFB_PID"

openbox &
OPENBOX_PID=$!
echo "Openbox started with PID $OPENBOX_PID"

cleanup() {
    echo "Stopping openbox and Xvfb..."
    kill $OPENBOX_PID 2>/dev/null || true
    kill $XVFB_PID 2>/dev/null || true
    exit
}

trap cleanup SIGINT SIGTERM EXIT

gunicorn -w 1 -b 0.0.0.0:5000 main:app
