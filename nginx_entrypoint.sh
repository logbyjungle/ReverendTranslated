#!/bin/sh
set -e

export TUNNEL_URL=$(cat /address.txt)

envsubst '${TUNNEL_URL}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'
