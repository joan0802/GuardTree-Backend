#!/bin/bash

# Check if running in Docker or locally
if [ -f /.dockerenv ]; then
  echo "Running tests inside Docker container"
  # Running inside Docker container
  pytest "$@"
else
  echo "Running tests via Docker"
  # Running locally, use docker exec
  docker compose exec -T api pytest "$@"
fi 