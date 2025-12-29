FROM python:3.12-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


FROM base AS test

COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt

COPY main.py ./
COPY src/ ./src/
COPY tests/ ./tests/

FROM base AS production

COPY main.py ./
COPY src/ ./src/