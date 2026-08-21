"""Resolve git refs and materialize them as build workspaces.

Because leapfrog-core, leapfrogr, and codegen all live in this one monorepo,
checking out a single commit gives every interface consistent with each
other as of that ref -- there's no cross-ref pinning problem to solve here.
"""

import hashlib
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

# The sentinel `<ref>` value meaning "the caller's own uncommitted checkout",
# rather than a committed git ref/SHA (ticket 19's Answer).
WORKING_TREE = "working-tree"

# Directories whose content actually feeds `build.build_leapfrogr` (codegen's
# input, its generated-header output's source, and leapfrogr itself) -- an
# uncommitted change outside these (e.g. to this CLI) shouldn't force a
# rebuild of the working-tree ref.
SOURCE_DIRS_FOR_HASH = ("leapfrog-core", "codegen", "leapfrogr")


class GitError(RuntimeError):
    """Raised when a git ref/SHA can't be resolved or a worktree can't be created."""


def find_repo_root(start: Path | None = None) -> Path:
    """Return the git repository root containing `start` (default: cwd)."""
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

    Only committed refs are supported; `WORKING_TREE` is handled separately
    by `prepare_source` since it has no SHA to resolve to.
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


def hash_source_dirs(repo_root: Path, subdirs: Sequence[str] = SOURCE_DIRS_FOR_HASH) -> str:
    """Content hash of `subdirs` under `repo_root`, as currently on disk (committed or not).

    Stands in for a commit SHA as `materialize_working_tree`'s cache key: a
    committed ref gets a free, cheap cache key from git; the working tree has
    none, so re-running against unchanged content must still hash identically
    for `build.build_leapfrogr`'s existing install-marker check to skip the
    rebuild, exactly as it would for an unchanged ref.
    """
    digest = hashlib.sha256()
    for subdir in subdirs:
        base = repo_root / subdir
        if not base.exists():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file()):
            digest.update(str(path.relative_to(repo_root)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def materialize_working_tree(repo_root: Path, cache_dir: Path) -> Path:
    """Copy the current uncommitted working tree into an isolated, content-keyed worktree.

    `build_leapfrogr` generates headers and installs into whatever worktree
    it's pointed at; pointing it at `repo_root` directly would write those
    build byproducts into the developer's real checkout. Keying the
    destination by `hash_source_dirs` (rather than a fixed path) means an
    unchanged working tree reuses the same destination -- and so the same
    install marker -- across repeated calls, while any relevant source change
    gets a fresh one.
    """
    dest = cache_dir / "worktrees" / f"{WORKING_TREE}-{hash_source_dirs(repo_root)}"
    if dest.exists():
        return dest

    dest.mkdir(parents=True)
    result = subprocess.run(
        ["rsync", "-a", "--exclude=.git", f"{repo_root}/", f"{dest}/"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        shutil.rmtree(dest, ignore_errors=True)
        msg = f"Could not materialize working tree from {repo_root} to {dest}:\n{result.stderr}"
        raise GitError(msg)
    return dest


def prepare_source(repo_root: Path, cache_dir: Path, ref: str) -> Path:
    """Resolve `ref` (a committed git ref/SHA, or `WORKING_TREE`) to a worktree to build from."""
    if ref == WORKING_TREE:
        return materialize_working_tree(repo_root, cache_dir)
    sha = resolve_ref(repo_root, ref)
    return ensure_worktree(repo_root, sha, cache_dir)
