# Referral Finder

## Overview

Referral Finder is a project designed to simplify the process of managing referrals. It comprises frontend and backend components that seamlessly run within Docker containers.

### Frontend

The `frontend` directory contains the client-side application, developed using React and JavaScript. This interface enables users to interact with Referral Finder, providing intuitive tools for searching, managing, and handling referrals.

### Backend

The `backend` directory houses the server-side application. Built on Django and FastAPI with two separate server, it manages data, user requests, and database interactions, providing essential endpoints and logic to support the frontend functionalities.

## Running the Project

### Prerequisites

Ensure the following dependencies are installed before running Referral Finder:

- Docker

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/referral-finder.git
   ```

2. **Build & Run Docker Containers**
   You need to build/run PostgreSQL, Redis, and RabbitMQ Container using official image before starting the project.
    ```bash
    docker run --name my-postgres -e POSTGRES_DB=['sceret'] -e POSTGRES_USER=['sceret] -e POSTGRES_PASSWORD=['sceret] -d postgres
    ````

    ```bash
    docker run -d --name my-redis -p 6379:6379 redis
    ````
    
     ```bash
    cd rabbit_container
    docker build -t rabbit .
    docker run -d -p 5672:5672 -p 10000:15672 --name rabbit-container rabbit
    cd ..
    ````
     
    ```bash
    docker build -t my-app:latest .
    ```
3. **Run Referral Docker Container**
   The provided script start_project.sh orchestrates the launch of various servers. Running this script initiates the simultaneous activation of Django, React, FastAPI, and Celery servers, facilitating a comprehensive web application setup. Moreover, this cohesive setup ensures continuous synchronization between your local development environment and the referral Docker container.

   Prior to executing the script, ensure you replace [my-postgres-ip], [my-redis-ip], and [rabbit-ip] with the respective IP addresses retrieved using the following commands:

   PostgreSQL IP: ``` docker inspect [my-postgres] | grep -i ipaddress```
   
   Redis IP: ```docker inspect [my-redis] | grep -i ipaddress```
   
   RabbitMQ IP: ```docker inspect [rabbit] | grep -i ipaddress```

   ```bash
       docker run --name referral
         -e DB_HOST='[my-postgres-ip]' \
         -e REDIS_HOST='[my-redis-ip]' \
         -e RABBIT_HOST='[rabbit-ip]'\
        -p 8088:8000 -p 8087:3000 -p 8002:8001 \
        -v .:/app
       my-app
   ```
   At this point, all four servers (Django, React, FastAPI, Celery) will be running in the terminal automatically.

4. **Manually Start the Server in Docker [Optional]**
   In case you need to manually start Django, React, FastAPI and Celery server, you can run the following commands:

   For Django (only when you first run the server or make changes to the Models):
    ```bash
    cd backend
    python manage.py makemigrations
    python manage.py migrate
    ```

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

5. **Navigate the App in Browser**
Frontend will be running on: 
```bash http://localhost:8087/```
