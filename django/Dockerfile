ARG ENVIRONMENT=prod

FROM python:3.8-alpine as base
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log

EXPOSE 8000
# Needed for better experience in container terminal
ENV TERM=xterm-256color

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ADD website/requirements /opt/requirements

RUN apk update
RUN apk add \
      bash \
      git wget \
      gcc libc-dev \
      python3-dev py3-pip \
      py3-greenlet py3-pillow \
      libffi-dev zlib-dev jpeg-dev \
      py3-cffi py3-cryptography

RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && python3 -m venv /env \
    && /env/bin/pip install --upgrade pip setuptools wheel

# Add bash aliases
ADD bash_aliases /root/.bash_aliases

FROM base as dev
# Update and install
RUN apk update
RUN apk add \
      bash \
      git wget \
      gcc libc-dev \
      python3-dev py3-pip \
      py3-greenlet py3-pillow \
      py3-cffi py3-cryptography

RUN set -ex \
    && /env/bin/pip install --no-cache-dir -r /opt/requirements/dev.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
# Set the needed variables
ENV PYTHONPATH=/app/wagtail_vue:/app/wagtail_vue/apps
ENV DJANGO_SETTINGS_MODULE=wagtail_vue.settings.dev

# change to /app for the working directory, you should mount the local dir volume here

WORKDIR /app

FROM base as prod

RUN set -ex \
    && /env/bin/pip install --no-cache-dir -r /opt/requirements/production.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
# Set the needed variables
ENV PYTHONPATH=/app/wagtail_vue:/app/wagtail_vue/apps
ENV DJANGO_SETTINGS_MODULE=wagtail_vue.settings.production

ADD website/ /app
# change to /app for the working directory, you should mount the local dir volume here
WORKDIR /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "wagtail_vue.wsgi:application"]

FROM ${ENVIRONMENT}