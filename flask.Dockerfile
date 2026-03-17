
FROM python:3.13-slim

WORKDIR /docker-flask

RUN apt-get update && apt-get install -y \
    wget unzip git gnupg ca-certificates \
    build-essential libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/* 

RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google.list \
    && apt-get update 

RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_145.0.7632.116-1_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_145.0.7632.116-1_amd64.deb \
    && rm google-chrome-stable_145.0.7632.116-1_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY static ./static
COPY templates ./templates
COPY languages.txt .
COPY main.py .
COPY bot.py .
COPY .git .git

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["gunicorn","-w","1","-k","sync","-b","0.0.0.0:5000","-t","120","main:app","--log-level","debug"]
