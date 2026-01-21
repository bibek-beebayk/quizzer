FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update \
  && apt-get install -y libmagic-dev gcc \
  && apt-get clean \
  && pip install --upgrade pip \
  && pip install -r requirements/frozen.txt


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]