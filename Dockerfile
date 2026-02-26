
FROM python:3.13-slim

WORKDIR /docker-flask

RUN apt-get update && apt-get install -y \
    # chromium chromium-driver wget unzip git \
    # chromium wget unzip git \
    wget unzip git \
    build-essential libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget gnupg \
    && wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

COPY static ./static
COPY templates ./templates
COPY languages.txt .
COPY main.py .
COPY bot.py .
# COPY .git ./.git
RUN if [ -d ".git" ]; then cp -r .git ./.git; fi

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["gunicorn","-w","1","-k","sync","-b","0.0.0.0:5000","-t","120","main:app","--log-level","debug"]
