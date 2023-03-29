FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y --no-install-recommends gettext

RUN pip install --upgrade pip && \
    pip install poetry==1.4.0

COPY poetry.lock pyproject.toml README.md /app/

RUN poetry export --with dev -f requirements.txt -o requirements.txt && \
    pip uninstall --yes poetry && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt




FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get install ruby --no-install-recommends -y && \
    gem install pact_broker-client

WORKDIR /app

RUN addgroup --system appuser && adduser --system --group appuser

COPY --chown=appuser --from=builder /app/wheels /wheels
COPY --chown=appuser --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

USER appuser


