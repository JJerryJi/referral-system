# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION} as base
# FROM test as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt install -y nodejs 

# Use production node environment by default.
ENV NODE_ENV production

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=backend/requirements.txt,target=backend/requirements.txt \
    python -m pip install -r backend/requirements.txt

WORKDIR /app/frontend 
RUN --mount=type=bind,source=frontend/package.json,target=package.json \
    --mount=type=bind,source=frontend/package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci

# Copy the source code into the container.
COPY ./backend /app/backend
COPY ./frontend /app/frontend

# Expose the port that the application listens on.
EXPOSE 8000 3000 8001

# Run the application.
CMD python /app/backend/manage.py runserver 0.0.0.0:8000 
# uvicorn websocket:app --reload --host 0.0.0.0 --port 8001