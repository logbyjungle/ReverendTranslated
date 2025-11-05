
FROM python:3.13-slim

WORKDIR /docker-flask

RUN apt-get update && apt-get install -y \
    chromium chromium-driver xvfb openbox wget unzip xclip git \
# idk how needed this is
    build-essential libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn gevent

COPY static ./static
COPY templates ./templates
COPY languages.txt .
COPY main.py .
COPY bot.py .
COPY .git ./.git

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV DISPLAY=:99

COPY entrypoint.sh .
RUN chmod +x /docker-flask/entrypoint.sh

ENTRYPOINT [ "/docker-flask/entrypoint.sh" ]
