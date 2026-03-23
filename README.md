DevOps Task Manager App 

Full-stack DevOps project demonstrating:
Flask web application (GUI),
PostgreSQL database,
Nginx reverse proxy,
Docker & Docker Compose,
Environment variables (.env),
Persistent storage (Docker volumes),
CI/CD with GitHub Actions

Architecture
User>Nginx>Flask>PostgreSQL

Run project:
docker compose up --build

This project includes a CI pipeline using GitHub Actions that:
builds Docker images,
starts full multi-container environment (Flask + PostgreSQL + Nginx),
waits for services to be ready,
tests application by HTTP request,
cleans up containers

[![CI Pipeline](https://github.com/kawkaAW/devops-simple-task-manager-app/actions/workflows/ci.yml/badge.svg)](https://github.com/kawkaAW/devops-simple-task-manager-app/actions/workflows/ci.yml)