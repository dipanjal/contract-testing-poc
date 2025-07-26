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
ENV_NAME="${PACT_BROKER_ENV_NAME:-test}"
PACT_DO_NOT_TRACK=1

# Reading current commit hash from git head
CONTRACT_VERSION=$(git rev-parse --short HEAD)

echo "Can I Deploy -> $PARTICIPANT Version: $CONTRACT_VERSION in ENV: $ENV_NAME"

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

# Check if can deploy
$PACT_CLI \
  pact-broker can-i-deploy \
  --broker-base-url "$PACT_BROKER_URL" \
  --broker-username "$PACT_BROKER_USERNAME" \
  --broker-password "$PACT_BROKER_PASSWORD" \
  --pacticipant "$PARTICIPANT" \
  --version "$CONTRACT_VERSION" \
  --to-environment "$ENV_NAME" \
  --retry-while-unknown 0 \
  --retry-interval 10
