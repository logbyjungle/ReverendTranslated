#!/bin/bash
set -e

envsubst '${DOMAIN}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/nginx.conf
envsubst '${DOMAIN}'< /etc/nginx/conf.d/nginx.conf.https.template > /etc/nginx/conf.d/nginx.conf.https

(
    while true; do
        sleep 12h
        certbot renew --quiet --deploy-hook "nginx -s reload"
    done
) &

exec nginx -g 'daemon off;'
