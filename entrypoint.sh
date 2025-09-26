#!/bin/bash
set -e

# Remove stale Xvfb lock if it exists
if [ -f /tmp/.X99-lock ]; then
    echo "Removing stale Xvfb lock"
    rm -f /tmp/.X99-lock
fi

Xvfb :99 -screen 0 1280x1024x24 &
XVFB_PID=$!
echo "Xvfb started with PID $XVFB_PID"

sleep 4

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

gunicorn -w 1 -b 0.0.0.0:5000 -t 120 main:app
