FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR root
COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

WORKDIR src
COPY src/ .
COPY pyproject.toml ./stub.toml

EXPOSE 7070
RUN pip install uvicorn
