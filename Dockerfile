FROM nginx:alpine

RUN apk add --no-cache bash gettext

COPY nginx_entrypoint.sh /nginx_entrypoint.sh
RUN chmod +x /nginx_entrypoint.sh

COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

EXPOSE 80

CMD ["./nginx_entrypoint.sh"]
