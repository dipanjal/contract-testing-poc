import os
import subprocess
from pathlib import Path
from traceback import print_tb

def execute_command(command_parts: list[str]) -> str:
    return subprocess.check_output(
        command_parts
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

# if __name__ == "__main__":
#     short_hash: str = git_revision_short_hash()
#     print(short_hash)
#     branch_name: str = git_revision_branch_name()
#     print(branch_name)
