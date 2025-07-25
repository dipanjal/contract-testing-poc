all: install

install:
	./scripts/install.sh

test:
	./scripts/test.sh

can-i-deploy:
	./scripts/can_i_deploy.sh

verify:
	./scripts/verify.sh

contract-test: test can-i-deploy verify

clean-pacts:
	@rm -rf ./src/consumer/pact-logs
	@rm -rf ./src/provider/pact-logs
	@rm -rf ./src/consumer/pacts

.PHONY: install test verify can-i-deploy contract-test clean-pacts
