"""Resolve git refs and materialize them as build workspaces.

Because leapfrog-core, leapfrogr, and codegen all live in this one monorepo,
checking out a single commit gives every interface consistent with each
other as of that ref -- there's no cross-ref pinning problem to solve here.
"""

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = f"'{start}' is not inside a git repository:\n{result.stderr}"
        raise GitError(msg)
    return Path(result.stdout.strip())


def resolve_ref(repo_root: Path, ref: str) -> str:
    """Resolve a committed git ref/SHA to its full commit SHA.

    Only committed refs are supported -- an uncommitted working tree is
    ticket 19, not this one.
    """
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "--verify", f"{ref}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = f"Could not resolve '{ref}' to a commit in {repo_root}:\n{result.stderr}"
        raise GitError(msg)
    return result.stdout.strip()


def ensure_worktree(repo_root: Path, sha: str, cache_dir: Path) -> Path:
    """Ensure a git worktree checked out at `sha` exists under `cache_dir`.

    Reused across calls for the same sha, so comparing two refs that
    resolve to the same commit (or repeat runs against an unchanged ref)
    skip the checkout.
    """
    worktree = cache_dir / "worktrees" / sha
    if worktree.exists():
        return worktree

    worktree.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "add", "--detach", str(worktree), sha],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = f"Could not create worktree for '{sha}' at {worktree}:\n{result.stderr}"
        raise GitError(msg)
    return worktree
