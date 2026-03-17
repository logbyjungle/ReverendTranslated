#!/bin/sh

CURRENT_URL=""

while true; do
    URL=$(curl -s "https://raw.githubusercontent.com/$REPO/tunnel/address.txt")
    if [ "$CURRENT_URL" != "$URL" ]; then
        export TUNNEL_URL="$URL"
        envsubst '${TUNNEL_URL}' < "/nginx.conf.template" > "/nginx.conf.template2"
        export TUNNEL_HOST=$(echo $TUNNEL_URL | awk -F/ '{print $3}')
        envsubst '${TUNNEL_HOST}' < "/nginx.conf.template2" > "/etc/nginx/conf.d/default.conf"

        if [ -z "$NGINX_STARTED" ]; then
            nginx -g 'daemon off;' &
            NGINX_STARTED=1
        else
            nginx -s reload
        fi
        CURRENT_URL="$URL"
        fi
    sleep 10
done
