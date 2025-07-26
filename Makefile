CONSUMER_NAME=transaction-service
PROVIDER_NAME=sync-service

all: init

start-broker:
	@docker-compose up -d

stop-broker:
	@docker-compose down

reboot-broker: stop-broker start-broker

install:
	./scripts/install.sh

clean-pacts:
	@rm -rf ./src/consumer/pact-logs
	@rm -rf ./src/provider/pact-logs
	@rm -rf ./src/consumer/pacts

test: clean-pacts
	./scripts/test.sh

init: start-broker install clean-pacts

can-i-deploy-consumer:
	PARTICIPANT=${CONSUMER_NAME} ./scripts/can_i_deploy.sh

can-i-deploy-provider:
	PARTICIPANT=${PROVIDER_NAME} ./scripts/can_i_deploy.sh

verify:
	./scripts/verify.sh

deploy-consumer:
	PARTICIPANT=${CONSUMER_NAME} ./scripts/deploy.sh

deploy-provider:
	PARTICIPANT=${PROVIDER_NAME} ./scripts/deploy.sh

contract-test: test can-i-deploy verify

.PHONY: start-broker stop-broker reboot-broker install init test verify can-i-deploy contract-test clean-pacts
