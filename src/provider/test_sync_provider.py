"""Module for Contracts (Pacts) verification."""

from pathlib import Path

import pytest
from pact import Verifier

from src import (
    PACT_BROKER_USERNAME,
    PACT_BROKER_PASSWORD,
    PACT_BROKER_URL,
    SYNC_SERVICE_URL
)

PROVIDER_NAME = "sync-provider"

CURRENT_DIR = Path(__file__).parent.resolve()

@pytest.fixture(scope="session")
def broker_opts(contract_version, contract_branch) -> dict:
    return {
        'broker_username': PACT_BROKER_USERNAME,
        'broker_password': PACT_BROKER_PASSWORD,
        'broker_url': PACT_BROKER_URL,
        'publish_version': contract_version,
        'provider_version_branch': contract_branch,
        'publish_verification_results': True,
    }

@pytest.fixture(scope="session")
def pact_log_dir() -> str:
    """Fixture for the Pact directory."""
    return str(CURRENT_DIR / "pact-logs")

@pytest.mark.verify_contract
def test_product_service_provider_against_broker(
    broker_opts: dict, pact_log_dir
):
    verifier = Verifier(
        provider=PROVIDER_NAME,
        provider_base_url=SYNC_SERVICE_URL,
    )

    result, _ = verifier.verify_with_broker(
        **broker_opts,
        verbose=False,
        provider_states_setup_url=f"{SYNC_SERVICE_URL}/_pact/provider_states",
        enable_pending=True,
        log_dir=pact_log_dir,
        consumer_selectors=[
            # Recommended.
            # Returns the pacts for consumers configured mainBranch property.
            {'mainBranch': True},

            # Recommended.
            # Returns the pacts for all versions of the consumer that are
            # currently deployed or released and currently supported in any
            # environment.
            {'deployedOrReleased': True},
        ]
    )

    # If publish_verification_results is set to True, the results will be
    # published to the Pact Broker. In the Pact Broker logs, this corresponds
    # to the following entry:
    #
    #    PactBroker::Verifications::Service -- Creating verification 200 for \
    #    pact_version_sha=c8568cbb30d2e3933b2df4d6e1248b3d37f3be34 -- \
    #    {"success"=>true, "providerApplicationVersion"=>"1.8.0+dc939d3", \
    #    "wip"=>false, "pending"=>"true"}
    #

    # Note:
    #
    #  If "successful", then the return code here will be 0.
    #  This can still be 0 and so PASS if a Pact verification FAILS, as long as
    #  it has not resulted in a REGRESSION of an already verified interaction.
    #  See https://docs.pact.io/pact_broker/advanced_topics/pending_pacts/ for
    #  more details.
    assert result == 0
