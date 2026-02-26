
FROM python:3.13-slim

WORKDIR /docker-flask

RUN apt-get update && apt-get install -y \
    # chromium chromium-driver wget unzip git \
    # chromium wget unzip git \
    wget unzip git \
    build-essential libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y curl unzip \
    && curl -LO https://storage.googleapis.com/chrome-for-testing-public/146.0.0.0/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip \
    && mv chrome-linux64 /opt/chrome

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
