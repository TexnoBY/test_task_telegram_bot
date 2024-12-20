FROM python:3.12-alpine

RUN apk update && apk add python3-dev gcc libc-dev
RUN apk add --no-cache git

WORKDIR /app
RUN pip install --upgrade pip

ADD . requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./alembic /app/alembic
ADD ./app /app/app
ADD ./docker /app/docker

RUN chmod +x /app/docker/server-entrypoint.sh