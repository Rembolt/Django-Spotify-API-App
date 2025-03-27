#!/bin/sh

set -e

# Generate Nginx config with environment variables
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Wait for SSL certificates
echo "Checking for SSL certificates..."
if [ ! -f "/etc/letsencrypt/live/powershuffle.ianblanc.com/fullchain.pem" ]; then
    echo "No SSL certificates found. Starting Nginx in HTTP mode..."
    nginx -g 'daemon off;'
else
    echo "SSL certificates found! Enabling HTTPS..."
    nginx -g 'daemon off;'
fi
