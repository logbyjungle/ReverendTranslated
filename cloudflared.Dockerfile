FROM alpine:3.18

RUN apk add --no-cache bash curl git

RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared \
    && chmod +x /usr/local/bin/cloudflared

COPY cloudflared_entrypoint.sh entrypoint.sh
COPY address.txt address.txt
COPY .git .git

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
