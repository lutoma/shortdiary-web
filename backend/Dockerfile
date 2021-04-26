FROM python:3.9-buster
LABEL maintainer="lukas@fnordserver.eu"
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN wget "https://caddyserver.com/api/download?os=linux&arch=amd64" -O /usr/local/bin/caddy
RUN chmod +x /usr/local/bin/caddy

RUN apt update && apt install -y supervisor redis-server git

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --no-cache-dir poetry
RUN poetry install
RUN poetry add gunicorn

COPY . .
RUN poetry run ./manage.py collectstatic --noinput

RUN mkdir -p /data/redis
RUN ln -s /data/settings_local.py shortdiary/settings_local.py
RUN ln -s /data/asset asset

RUN git rev-parse --short HEAD > templates/current_git_version.txt
CMD ["/usr/bin/supervisord", "-c", "/code/supervisord.conf"]
