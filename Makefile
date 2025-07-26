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

can-i-deploy:
	./scripts/can_i_deploy.sh

verify:
	./scripts/verify.sh

deploy-provider:
	./scripts/deploy_provider.sh

deploy-consumer:
	./scripts/deploy_consumer.sh

contract-test: test can-i-deploy verify

.PHONY: start-broker stop-broker reboot-broker install init test verify can-i-deploy contract-test clean-pacts
