# Referral Finder

## Overview

Referral Finder is a project designed to simplify the process of managing referrals. It comprises frontend and backend components that seamlessly run within Docker containers.

### Frontend

The `frontend` directory contains the client-side application, developed using [insert framework/language here]. This interface enables users to interact with Referral Finder, providing intuitive tools for searching, managing, and handling referrals.

### Backend

The `backend` directory houses the server-side application. Built on [insert language/framework here], it manages data, user requests, and database interactions, providing essential endpoints and logic to support the frontend functionalities.

## Running the Project

### Prerequisites

Ensure the following dependencies are installed before running Referral Finder:

- Docker

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/referral-finder.git
   ```

2. **Build Docker Containers**
You need to build/run PostgreSQL, Redis, and RabbitMQ Container using official image before starting the project.
    ```bash
    docker run --name my-postgres -d postgres :5432
    ````
    
    ```bash
    docker run --name my-redis -d redis -p 6379:6379
    ````
    
     ```bash
    cd rabbit_container; docker build -t rabbit -p 5672:5672 -p 10000:15672; cd ..
    ````
     
    ```bash
    docker build -t my-app:latest .
    ```
3. **Run Docker Container**
You need to find the respective IPAddress of PostgreSQL, Redis, and RabbitMQ container using ```bash  docker inspect [my-postgres|my-redis|rabbit] | grep -i ipaddress```
    ```bash
    docker run --rm --name referral
      -e DB_HOST='[my-postgres-ip]' \
      -e REDIS_HOST='[my-redis-ip]' \
      -e RABBIT_HOST='[rabbit-ip]'\
     -p 8088:8000 -p 8087:3000 -p 8002:8001 my-app
    ```
At this point, Django server is running in the terminal.

4. **Start the Server**
Finally, you need to start React server, FastAPI server and Celery server, which provides frontend UI, websocket, ane async email service in other terminal.
For React:
    ```bash
    cd frontend
    npm start
    ```
For FastAPI:
    ```bash
    cd backend
    uvicorn websocket:app --reload --host 0.0.0.0 --port 8001
    ```
For Celery:
  ```bash
  cd backend
  celery -A referral worker --loglevel=INFO
  ```

