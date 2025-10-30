#!/bin/bash
set -e

certbot certonly --non-interactive --agree-tos --email "$EMAIL" --preferred-challenges dns --authenticator dns-duckdns --dns-duckdns-token "$TOKEN" --dns-duckdns-propagation-seconds 60 -d "$DOMAIN"
cd etc/nginx/conf.d/
mv nginx.conf nginx.conf.disabled
mv nginx.conf.https nginx.conf
nginx -s reload
