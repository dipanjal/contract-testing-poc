"""Module for Contracts (Pacts) verification."""

from pathlib import Path

import pytest
from pact import Verifier

from src.provider import APP_NAME
from src.provider.constants import (
    PACT_BROKER_USERNAME,
    PACT_BROKER_PASSWORD,
    PACT_BROKER_URL,
    SELF_HOST_URL
)

PROVIDER_NAME = APP_NAME

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
    return str(CURRENT_DIR / "pact-logs")

@pytest.mark.verify_contract
def test_product_service_provider_against_broker(
    broker_opts: dict, pact_log_dir
):
    verifier = Verifier(
        provider=PROVIDER_NAME,
        provider_base_url=SELF_HOST_URL,
    )

    result, _ = verifier.verify_with_broker(
        **broker_opts,
        verbose=False,
        provider_states_setup_url=f"{SELF_HOST_URL}/_pact/provider_states",
        enable_pending=True,
        log_dir=pact_log_dir,
        consumer_selectors=[
            {'mainBranch': True},
            {'deployedOrReleased': True},
        ]
    )
    assert result == 0
