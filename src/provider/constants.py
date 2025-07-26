from os import environ

# Broker Constants
PACT_BROKER_URL = environ.get('PACT_BROKER_URL', 'http://localhost:9292')
PACT_BROKER_USERNAME = environ.get('PACT_BROKER_USERNAME', 'pactbroker')
PACT_BROKER_PASSWORD = environ.get('PACT_BROKER_PASSWORD', 'pactbroker')

# Provider Constants
# Though it will be running locally still reading from env
# incase the verification process runs inside a docker-compose environment
# and the URL is passed by the environment
SELF_HOST_URL = environ.get("SYNC_SERVICE_URL", "http://localhost:5000")