import pytest

from src.common_utils import git_revision_short_hash, git_revision_branch_name

@pytest.fixture(scope='session')
def contract_version() -> str:
    return git_revision_short_hash()

@pytest.fixture(scope='session')
def contract_branch() -> str:
    return git_revision_branch_name()
