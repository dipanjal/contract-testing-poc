from pathlib import Path

import pytest
from pact import Consumer, Provider, Term, Format, Like, Pact

from src import PACT_BROKER_URL, PACT_BROKER_USERNAME, PACT_BROKER_PASSWORD, APP_VERSION, APP_BRANCH
from src.consumer.sync_service_client import SimpleSyncServiceClient

# Mock Server Constants
MOCK_SERVER_HOST = "localhost"
MOCK_SERVER_PORT = 1234
MOCK_SERVER_URL = f"http://{MOCK_SERVER_HOST}:{MOCK_SERVER_PORT}"

CURRENT_DIR = Path(__file__).parent.resolve()

@pytest.fixture(scope="session")
def pact_dir() -> str:
    """Fixture for the Pact directory."""
    return str(CURRENT_DIR / "pacts")


@pytest.fixture(scope="session")
def pact_log_dir() -> str:
    """Fixture for the Pact directory."""
    return str(CURRENT_DIR / "pact-logs")


@pytest.fixture(scope="session")
def broker_opts() -> dict[str, any]:
    return dict(
        broker_base_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
        publish_to_broker=True,
    )

@pytest.fixture(scope="session")
def mock_server(pact_dir, pact_log_dir, broker_opts):
    pact: Pact = Consumer(
        "transaciton-sync-consumer",
        version=APP_VERSION,
        branch=APP_BRANCH
    ).has_pact_with(
        provider=Provider("sync-provider"),
        host_name=MOCK_SERVER_HOST,
        port=MOCK_SERVER_PORT,
        pact_dir=pact_dir,
        log_dir=pact_log_dir,
        **broker_opts
    )
    try:
        pact.start_service()
        yield pact
    finally:
        pact.stop_service()

class TestSyncServiceConsumer:
    def setup_method(self):
        """Setup for each test method"""
        self.client = SimpleSyncServiceClient(MOCK_SERVER_URL)

    @pytest.mark.asyncio
    async def test_get_version(self, mock_server):
        """Test getting version information from sync-service"""
        # Define the expected interaction
        expected_version = {
            'service': Term(
                matcher=r'^sync-service$',
                generate='sync-service'
            ),
            'version': Term(
                matcher=r'^\d+(.\d+){2,3}$',
                generate='1.0.0'
            ),
            'build': Term(
                matcher=r'^\d{8}-[a-f0-9]+$',
                generate='20240101-abc123'
            ),
            'timestamp': Format().iso_8601_datetime(with_ms=True)
        }

        (
            mock_server
            .given('sync-service is running')
            .upon_receiving('a request for version information')
            .with_request(
                method='GET',
                path='/version'
            )
            .will_respond_with(
                status=200,
                headers={'Content-Type': 'application/json'},
                body=Like(expected_version)
            )
        )

        # Start the mock server and run the test
        with mock_server:
            result = await self.client.get_version()

            # Verify the response structure
            assert result['service'] == 'sync-service'
            assert isinstance(result['version'], str)
            assert isinstance(result['build'], str)
            assert isinstance(result['timestamp'], str)

    # @pytest.mark.asyncio
    # async def test_get_version_service_unavailable(self, pact):
    #     """Test handling when sync-service is unavailable"""
    #     (pact
    #      .given('sync-service is unavailable')
    #      .upon_receiving('a request for version when service is down')
    #      .with_request(
    #          method='GET',
    #          path='/version'
    #      )
    #      .will_respond_with(
    #          status=503,
    #          headers={'Content-Type': 'application/json'},
    #          body={
    #              'error': 'Service temporarily unavailable'
    #          }
    #      ))
    #
    #     with pact:
    #         # Test that the client properly handles 503 errors
    #         with pytest.raises(aiohttp.ClientResponseError) as exc_info:
    #             await self.client.get_version()
    #
    #         assert exc_info.value.status == 503
    #
    #         pact.verify()
