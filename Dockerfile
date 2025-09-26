
FROM python:3.13

WORKDIR /docker-flask

RUN apt-get update && apt-get install -y \
    chromium chromium-driver xvfb openbox wget unzip xclip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

COPY . .

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV DISPLAY=:99

COPY ./entrypoint.sh /docker-flask/entrypoint.sh
RUN chmod +x /docker-flask/entrypoint.sh

ENTRYPOINT [ "/docker-flask/entrypoint.sh" ]
