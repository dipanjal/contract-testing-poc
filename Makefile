all: install

install:
	./scripts/install.sh

test:
	./scripts/test.sh

can-i-deploy:
	./scripts/can_i_deploy.sh

verify:
	./scripts/verify.sh

clean-pacts:
	@ rm -rf ./src/consumer/pact-logs
	@ rm -rf ./src/consumer/pacts
	@ rm -rf ./src/provider/pacts-logs

.PHONY: install test verify
