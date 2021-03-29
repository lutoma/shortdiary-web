FROM python:2.7-buster
LABEL maintainer="lukas@fnordserver.eu"
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . /code/

RUN pip install --no-cache-dir poetry
RUN poetry install
RUN poetry add gunicorn
RUN poetry run ./manage.py collectstatic --noinput

RUN mkdir /data
RUN ln -s /data/settings_local.py shortdiary/settings_local.py
RUN ln -s /data/asset asset

RUN wget "https://caddyserver.com/api/download?os=linux&arch=amd64" -O /usr/local/bin/caddy
RUN chmod +x /usr/local/bin/caddy

RUN apt update && apt install -y supervisor redis-server
CMD ["/usr/bin/supervisord", "-c", "/code/supervisord.conf"]
