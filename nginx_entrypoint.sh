#!/bin/sh
set -e

CURRENT_URL=""

while true; do
    URL=$(curl -s "https://raw.githubusercontent.com/$REPO/tunnel/address.txt")
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
    if [ "$HTTP_STATUS" = "200" ]; then
        if [ "$CURRENT_URL" != "$URL" ]; then
            export TUNNEL_URL="$URL"
            envsubst '${TUNNEL_URL}' < "/nginx.conf.template" > "/etc/nginx/conf.d/default.conf"

            if [ -z "$NGINX_STARTED" ]; then
                nginx -g 'daemon off;' &
                NGINX_STARTED=1
            else
                nginx -s reload
            fi
            CURRENT_URL="$URL"
        fi
    fi
    sleep 10
done

nginx -g 'daemon off;'
