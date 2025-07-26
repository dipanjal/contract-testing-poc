from fastapi import APIRouter, HTTPException
from typing import TYPE_CHECKING, Dict, Any
from pydantic import BaseModel

from src.provider.sync_controller import VersionResponse

if TYPE_CHECKING:
    pass

router = APIRouter(tags=["Provider State"])


class ProviderState(BaseModel):
    """Define the provider state."""

    consumer: str
    state: str


@router.post("/_pact/provider_states")
async def mock_pact_provider_states(
    state: ProviderState,
) -> Dict[str, Any]:
    """
    Define the provider state.

    For Pact to be able to correctly test compliance with the contract, the
    internal state of the provider needs to be set up correctly. Naively, this
    would be achieved by setting up the database with the correct data for the
    test, but this can be slow and error-prone. Instead this is best achieved by
    mocking the relevant calls to the database so as to avoid any side effects.

    For Pact to be able to correctly get the provider into the correct state,
    this function is used to define an additional endpoint on the provider. This
    endpoint is called by Pact before each test to ensure that the provider is
    in the correct state.
    """
    mapping = {
        "sync-service is running": mock_version_info_success,
        # "sync-service is unavailable": mock_service_unavailable,
    }
    
    if state.state not in mapping:
        raise HTTPException(
            status_code=400, 
            detail=f"Unknown provider state: {state.state}"
        )
    
    schema: BaseModel = mapping[state.state]()
    return schema.model_dump(exclude_none=True)


def mock_version_info_success() -> VersionResponse:
    """Mock the provider state for sync-service is running."""
    data = {
        "service": "sync-service",
        "version": "1.0.0",
        "build": "20240101-abc123",
        "timestamp": "2025-07-24T15:43:24.204757Z"
    }
    return VersionResponse(**data)


# def mock_service_unavailable() -> Dict[str, Any]:
#     """Mock the provider state for sync-service is unavailable."""
#     return {
#         'error': 'Service temporarily unavailable'
#     }
