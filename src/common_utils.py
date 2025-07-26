import subprocess
from pathlib import Path


def execute_command(command_segments: list[str]) -> str:
    return subprocess.check_output(
        command_segments
    ).decode("ascii").strip()

def git_revision_short_hash() -> str:
    """Get the short Git commit."""
    project_root = str(Path(__file__).parent.parent.resolve())

    return execute_command(
        ['git', '-C', project_root, 'rev-parse', '--short', 'HEAD']
    )

def git_revision_branch_name() -> str:
    """Get the short Git commit."""
    project_root = str(Path(__file__).parent.parent.resolve())

    return execute_command(
        ['git', '-C', project_root, 'rev-parse', '--abbrev-ref', 'HEAD']
    )
