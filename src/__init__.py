from os import environ

# App Constants
APP_VERSION = "1.0.0"  # TODO: this should be short git commit hash

# Consumer Constants
CONSUMER_NAME = "transaciton-sync-consumer"

# Broker Constants
PACT_BROKER_URL = environ.get('PACT_BROKER_URL', 'http://localhost:9292')
PACT_BROKER_USERNAME = environ.get('PACT_BROKER_USERNAME', 'pactbroker')
PACT_BROKER_PASSWORD = environ.get('PACT_BROKER_PASSWORD', 'pactbroker')

# Provider Constants
SYNC_SERVICE_URL = environ.get("SYNC_SERVICE_URL", "http://localhost:5000")
