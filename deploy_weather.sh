#!/bin/bash

# Navigate to your project directory
cd /path/to/your/project

# Pull the latest changes from the repository
git pull origin master

# Stop and remove existing containers
docker-compose down

# Rebuild and start the containers
docker-compose up -d --build
