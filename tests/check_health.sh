#!/bin/bash

MAX_ATTEMPTS=30
SLEEP_INTERVAL=2

echo "Checking if app is healthy..."

for i in $(seq 1 $MAX_ATTEMPTS); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
  
    if [ "$STATUS" -eq 200 ]; then
        echo "✅ App is healthy!"
        exit 0
    else
        echo "Waiting for app... (attempt $i)"
        sleep $SLEEP_INTERVAL
    fi
done

echo "❌ App did not become healthy in time."
exit 1
