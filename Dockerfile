FROM nginx:alpine

RUN apk add --no-cache bash gettext

COPY nginx_entrypoint.sh /start.sh
RUN chmod +x /nginx_entrypoint.sh

COPY nginx.template.conf /etc/nginx/templates/nginx.template.conf

EXPOSE 80

CMD ["./nginx_entrypoint.sh"]
