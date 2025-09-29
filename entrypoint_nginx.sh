#!/bin/bash
set -e

nginx

while true; do
    sleep 12h
    certbot renew --quiet --deploy-hook "nginx -s reload"
done
