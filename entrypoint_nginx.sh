#!/bin/bash
set -e

nginx

while true; do
    certbot renew --quiet --deploy-hook "nginx -s reload"
    sleep 12h
done
