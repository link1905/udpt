FROM node:10-stretch-slim as client-builder

WORKDIR /app
COPY . /app

# Python build stage
FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG COMPOSE_UID=1001
ARG COMPOSE_GID=1001

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # libmagic
  && apt-get install -y --no-install-recommends libmagic1 \
  # bjoern dependencies
  && apt-get install -y libev-dev \
  # healcheck tool
  && apt-get install -y curl \
# git
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

COPY --chown=${COMPOSE_UID}:${COMPOSE_GID} ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=${COMPOSE_UID}:${COMPOSE_GID} ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --from=client-builder --chown=${COMPOSE_UID}:${COMPOSE_GID} /app /app

RUN mkdir -p /app/media

RUN chown -R ${COMPOSE_UID}:${COMPOSE_GID} /app/media

USER ${COMPOSE_UID}:${COMPOSE_GID}

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
