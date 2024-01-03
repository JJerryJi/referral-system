# Referral Finder

## Overview

Referral Finder, a project focused on streamlining the process of obtaining industry referrals, utilizes a microservices architecture containerized with Docker. This architecture ensures modularity and ease of deployment. 

For deployment, the project leverages Helm, a tool that simplifies the management of Kubernetes applications, on Amazon Web Services (AWS) Elastic Kubernetes Service (EKS). It employs Kubernetes resources like Deployment for managing stateless applications, StatefulSet for stateful applications, and Service for networking. 

Additionally, Kubernetes Ingress is implemented for external access. This configuration not only facilitates efficient load balancing but also ensures the effective routing of external traffic to the appropriate microservices, enhancing overall system performance and reliability.

## Demo Pages

### Referral Post DashBoard
<img width="1437" alt="image" src="https://github.com/JJerryJi/referral-system/assets/106227061/582bf793-c950-4643-ab88-5ba02d69b3a8">

### Referral Post LeaderBoard 
<img width="1439" alt="image" src="https://github.com/JJerryJi/referral-system/assets/106227061/4a8d50b7-ab39-4b3e-9bc5-f51cbca04cd1">

### Publish Referral Post
<img width="1439" alt="image" src="https://github.com/JJerryJi/referral-system/assets/106227061/82e3b2bb-7c48-4dc2-bfd2-bbef5b8ce04d">

### View My Published Posts
<img width="1439" alt="image" src="https://github.com/JJerryJi/referral-system/assets/106227061/4dd15d15-42a6-4e22-a246-6feac2f7f499">

### View Applications
<img width="1439" alt="image" src="https://github.com/JJerryJi/referral-system/assets/106227061/32841381-f1aa-4900-811a-ec02070ee9e7">

### Favorite Referral Posts
<img width="1439" alt="image" src="https://github.com/JJerryJi/referral-system/assets/106227061/63cbddc6-500d-4c3b-a85a-6a3d1275399f">

### And More ...
Please checkout the demo

## Repo Structure 
---------------------------
### frontend

The `frontend` directory contains the client-side application, developed using React and JavaScript. This interface enables users to interact with Referral Finder, providing intuitive tools for searching, managing, and handling referrals.

### backend

The `backend` directory houses the server-side application. Built on Django and FastAPI with two separate server, it manages data, user requests, and database interactions, providing essential endpoints and logic to support the frontend functionalities.

### docs

This folder contains the documentation of this projects, including the API endpoint specification and project structure.

### helm

This folder hosts required files of `Helm` for the deployment of Kubernetes on AWS EKS server.


# Running the project
-------------------------- 
## 1. Using localhost

### Steps:

   1. Checkout to the tag 0.0.1
      ```bash
      git clone https://github.com/yourusername/referral-finder.git
      git checkout v0.0.1
      ```
  2. Install the required dependencies for backend and frontend
     ```bash
     [in correct directory]
     pip install backend/requirements.txt
     npm install
     ```
  3. Run server on localhost:3000 and localhost:8000
     ```bash
     [in correct directory]
     python manage.py runserver
     npm start
     uvicorn websocket:app --reload --port 8001
     ``` 

## 2. Using AWS EKS

Please checkout the `deployment.md` for more details

------------------------------- 

## 3. Using Docker Container
------------------------------- 
### Prerequisites

Ensure the following dependencies are installed before running Referral Finder:
- Docker 

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/referral-finder.git
   git checkout docker
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
