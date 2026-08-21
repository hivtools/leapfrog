"""Shared subprocess-run-and-check helper.

Every module here shells out to git/uv/R and needs the same failure shape
(exit code, full stdout/stderr, command, cwd) surfaced as a domain-specific
exception.
"""

import subprocess
from pathlib import Path


def run_checked(
    cmd: list[str],
    cwd: Path,
    error_cls: type[Exception],
    env: dict | None = None,
    error_context: str = "",
) -> subprocess.CompletedProcess:
    """Run `cmd`, raising `error_cls` with full command/cwd/stdout/stderr on a nonzero exit."""
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        msg = (
            f"{error_context} failed (exit {result.returncode})\n"
            f"command: {' '.join(cmd)}\n"
            f"cwd: {cwd}\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
        raise error_cls(msg)
    return result
