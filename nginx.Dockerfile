
FROM nginx:latest

RUN rm -f /etc/nginx/conf.d/default.conf

COPY ./nginx.conf.template /etc/nginx/conf.d/default.conf.template
COPY ./nginx.conf.https.template /etc/nginx/conf.d/nginx.conf.https.template
COPY ./activate_https.sh /activate_https.sh
RUN chmod +x /activate_https.sh
COPY ./disable_https.sh /disable_https.sh
RUN chmod +x /disable_https.sh

RUN apt-get update && apt-get install -y certbot \
    python3-certbot-nginx python3-minimal python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages certbot_dns_duckdns

COPY ./entrypoint_nginx.sh /nginxentrypoint/entrypoint.sh
RUN chmod +x /nginxentrypoint/entrypoint.sh

ENTRYPOINT [ "/nginxentrypoint/entrypoint.sh" ]
