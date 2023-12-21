#!/bin/bash
set -e

export DOCKER_BUILDKIT=1
{
  echo "Making migrations..."
  docker compose run --rm django python manage.py makemigrations
  docker compose run --rm django python manage.py migrate
  echo "Loading site information..."
  docker compose run --rm django python manage.py loaddata sites.json
  echo "Creating superuser..."
  docker compose run --rm django python manage.py createsuperuser --no-input
  echo "Loading users and projects..."
  docker compose run --rm django python manage.py loaddata users.json projects.json
  docker compose up --detach
} || {
  echo "Making migrations..."
  docker-compose run --rm django python manage.py makemigrations
  docker-compose run --rm django python manage.py migrate
  echo "Loading site information..."
  docker-compose run --rm django python manage.py loaddata sites.json
  echo "Creating superuser..."
  docker-compose run --rm django python manage.py createsuperuser --no-input
  echo "Loading users and projects..."
  docker-compose run --rm django python manage.py loaddata users.json projects.json
  docker-compose up --detach
}