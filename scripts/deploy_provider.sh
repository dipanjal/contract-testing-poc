#!/bin/bash

# Add local environment variables from container-local.env
local_env_file="./envs/local.env"
if [ -f "$local_env_file" ]; then
    # Read the file line by line
    while IFS= read -r line; do
        export "$line"
    done < "$local_env_file"
else
    echo "Error: $local_env_file does not exist."
fi

# ENV variables
PACT_BROKER_URL=${PACT_BROKER_CONTAINER_URL:-http://broker:9292}
PACT_BROKER_USERNAME="${PACT_BROKER_USERNAME:-pactbroker}"
PACT_BROKER_PASSWORD="${PACT_BROKER_PASSWORD:-pactbroker}"
DEPLOYMENT_ENV="${PACT_BROKER_ENV_NAME:-test}"

# Constants
APP_NAME="sync-service"
PACT_DO_NOT_TRACK=1
CONTRACT_VERSION=$(git rev-parse --short HEAD)

# FIND Docker Network
PROJECT_NAME=$(basename "$(pwd)")  # Get current directory name (project name)
DOCKER_NETWORK=$(docker network ls --format "{{.Name}}" | grep "^${PROJECT_NAME}_")  # Find and return just the network name
if ! [ -n "$DOCKER_NETWORK" ]; then
    echo "No network found for project: $PROJECT_NAME" >&2
    exit 1
fi

# Pact CLI in Docker
PACT_CLI="docker run --rm \
  --network $DOCKER_NETWORK \
  -e PACT_BROKER_BASE_URL=$PACT_BROKER_URL \
  -e PACT_BROKER_USERNAME=$PACT_BROKER_USERNAME \
  -e PACT_BROKER_PASSWORD=$PACT_BROKER_PASSWORD \
  -e PACT_DO_NOT_TRACK=$PACT_DO_NOT_TRACK \
  pactfoundation/pact-cli:latest"

$PACT_CLI \
pact-broker record-deployment \
  --broker-base-url "$PACT_BROKER_URL" \
  --broker-username "$PACT_BROKER_USERNAME" \
  --broker-password "$PACT_BROKER_PASSWORD" \
  --pacticipant "$APP_NAME" \
  --version "$CONTRACT_VERSION" \
  --environment "$DEPLOYMENT_ENV"