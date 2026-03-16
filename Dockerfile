FROM nginx:alpine

RUN apk add --no-cache bash gettext curl

COPY nginx_entrypoint.sh /nginx_entrypoint.sh
RUN chmod +x /nginx_entrypoint.sh

COPY nginx.conf.template /nginx.conf.template

EXPOSE 80

CMD ["/nginx_entrypoint.sh"]
