# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a user with elevated privileges
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.

RUN apt install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt install -y nodejs

# Use production node environment by default.
ENV NODE_ENV production

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=backend/requirements.txt,target=backend/requirements.txt \
    python -m pip install -r backend/requirements.txt

# Copy the source code into the container.
COPY ./backend ./backend

WORKDIR /app/frontend 
RUN --mount=type=bind,source=frontend/package.json,target=package.json \
    --mount=type=bind,source=frontend/package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci
RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache

# Switch to the non-privileged user to run the application.
USER appuser

COPY ./frontend .

# Expose the port that the application listens on.
EXPOSE 8000 3000

# Run the application.
CMD python /app/backend/manage.py runserver 0.0.0.0:8000