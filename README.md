# DevOps Health Dashboard

Real-time system metrics dashboard built as a DevOps portfolio project.
Monitors CPU, RAM, disk and load average with a live web interface.

## Architecture
```
Browser → Nginx (port 8080) → Flask API → Bash scripts
                                    ↓
                                  Redis (cache)
```

## Stack

![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

## Quick start
```bash
git clone git@github.com:Nezareth07/devops-health-dashboard.git
cd devops-health-dashboard
cp .env.example .env
docker compose up -d --build
open http://localhost:8080
```

## Features

- Live metrics: CPU, RAM, disk, load average and uptime
- Redis caching — configurable TTL to reduce system calls
- Health endpoints for all services
- Nginx reverse proxy — single entry point for web and API
- GitFlow versioning with conventional commits

## Project structure
```
api/          Flask API with Redis caching
nginx/        Reverse proxy + static dashboard
scripts/      Bash metrics collector
```# DevOps Health Dashborad
