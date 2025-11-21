#!/bin/bash
set -e

file="protocol.txt"
dir="$PWD"

if [ -f "$file" ]; then
    value=$(cat "$file")
else
    value=0
    echo 0 > "$file"
fi

if [ "$value" -eq 2 ]; then
    cd etc/nginx/conf.d/
    mv nginx.conf nginx.conf.https
    mv nginx.conf.disabled nginx.conf
    nginx -s reload
    cd "$dir"
    echo 1 > "$file"
fi
