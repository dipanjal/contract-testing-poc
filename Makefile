all: init

run-broker:
	@docker-compose up -d

stop-broker:
	@docker-compose down

install:
	./scripts/install.sh

clean-pacts:
	@rm -rf ./src/consumer/pact-logs
	@rm -rf ./src/provider/pact-logs
	@rm -rf ./src/consumer/pacts

test:
	./scripts/test.sh

init: run-broker install clean-pacts

reboot: stop-broker init

can-i-deploy:
	./scripts/can_i_deploy.sh

verify:
	./scripts/verify.sh

contract-test: test can-i-deploy verify

.PHONY: run-broker stop-broker install init test verify can-i-deploy contract-test clean-pacts
