#!/bin/bash
set -e

file="protocol.txt"
dir="$PWD"

# 0 is no https. 1 is https has been enabled and then disabled. 2 is https is fully enabled

if [ -f "$file" ]; then
    value=$(cat "$file")
else
    value=0
fi

if [ "$value" -eq 0 ]; then
    certbot certonly --non-interactive --agree-tos --email "$EMAIL" --preferred-challenges dns --authenticator dns-duckdns --dns-duckdns-token "$TOKEN" --dns-duckdns-propagation-seconds 60 -d "$DOMAIN"
fi

if [ "$value" -lt 2 ]; then
    cd etc/nginx/conf.d/
    mv nginx.conf nginx.conf.disabled
    mv nginx.conf.https nginx.conf
    nginx -s reload
fi

cd "$dir"
echo 2 > "$file"
