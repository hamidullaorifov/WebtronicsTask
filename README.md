# FastAPI Application

This repository contains a FastAPI application that you can run on your local machine. FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Prerequisites

To run this FastAPI application using Docker, you need to have the following software installed on your machine:

- Docker

If you don't have Docker installed, you can download and install it from the [official Docker website](https://www.docker.com/get-started).

## Getting Started

To run the FastAPI application on your local machine, follow these steps:

1. Clone this repository to your local machine or download the ZIP file and extract it.

```bash
git clone https://github.com/hamidullaorifov/WebtronicsTask.git
```

2. Open a terminal or command prompt and navigate to the project's directory.

```bash
cd WebtronicsTask
```

3. Build and run the Docker containers using Docker Compose.
```bash
docker-compose up -d
```
This command will build the necessary images and start the containers in detached mode.

4. Once the containers are running, you can access the FastAPI application by opening your web browser and navigating to http://localhost:8000.

## API Endpoints

This FastAPI application provides the following API endpoints:

- `POST /signup`: Endpoint to register new user.
- `POST /token`: Endpoint that returns access token.
- `GET /posts`: Endpoint that returns all posts list.
- `POST /posts`: Endpoint to create new post.
- `GET /posts/{id}`: Endpoint that returns details of a specific post.
- `PUT /posts/{id}`: Endpoint to update specific post.
- `DELETE /posts/{id}`: Endpoint to delete a specific post.
- `POST /posts/{id}/like`: Endpoint to like a specific post.
- `POST /posts/{id}/dislike`: Endpoint to dislike a specific post.

