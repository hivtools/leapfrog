import subprocess

import pytest

from leapfrog_validate import git_utils


@pytest.fixture
def repo_root():
    return git_utils.find_repo_root()


def test_resolve_ref_head_matches_git_rev_parse(repo_root):
    expected = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert git_utils.resolve_ref(repo_root, "HEAD") == expected
    assert len(git_utils.resolve_ref(repo_root, "HEAD")) == 40


def test_resolve_ref_unknown_ref_raises(repo_root):
    with pytest.raises(git_utils.GitError):
        git_utils.resolve_ref(repo_root, "definitely-not-a-real-ref-xyz")


def test_ensure_worktree_is_idempotent(repo_root, tmp_path):
    sha = git_utils.resolve_ref(repo_root, "HEAD")
    first = git_utils.ensure_worktree(repo_root, sha, tmp_path)
    second = git_utils.ensure_worktree(repo_root, sha, tmp_path)
    assert first == second
    assert (first / ".git").exists()

    subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "remove", "--force", str(first)],
        check=True,
    )
