FROM python:3.7.3-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=0.12.12
ENV PATH=$PATH:/usr/src/app

COPY . .

RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends git gcc \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config repositories.testpypi https://test.pypi.org/legacy/ \
    && poetry config settings.virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && apt-get remove -y --purge git gcc \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
