
FROM nginx:latest

RUN rm -f /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx.conf.https /etc/nginx/conf.d/nginx.conf.https

RUN apt-get update && apt-get install -y certbot \
    python3-certbot-nginx python3-minimal python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages certbot_dns_duckdns

COPY ./entrypoint_nginx.sh /nginxentrypoint/entrypoint.sh
RUN chmod +x /nginxentrypoint/entrypoint.sh

ENTRYPOINT [ "/nginxentrypoint/entrypoint.sh" ]
