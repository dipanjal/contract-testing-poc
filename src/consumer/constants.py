# Mock Server Constants
from os import environ

MOCK_SERVER_HOST = "localhost"
MOCK_SERVER_PORT = 1234
MOCK_SERVER_URL = f"http://{MOCK_SERVER_HOST}:{MOCK_SERVER_PORT}"

# Broker Constants
PACT_BROKER_URL = environ.get('PACT_BROKER_URL', 'http://localhost:9292')
PACT_BROKER_USERNAME = environ.get('PACT_BROKER_USERNAME', 'pactbroker')
PACT_BROKER_PASSWORD = environ.get('PACT_BROKER_PASSWORD', 'pactbroker')
PUBLISH_TO_BROKER: bool = bool(environ.get('PUBLISH_TO_BROKER', 1))

# Provider Constants
SYNC_SERVICE_URL = environ.get("SYNC_SERVICE_URL", "http://localhost:5000")
SYNC_SERVICE_NAME = "sync-service"