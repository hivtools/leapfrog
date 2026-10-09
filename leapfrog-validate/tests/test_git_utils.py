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


@pytest.fixture
def fake_source_tree(tmp_path):
    """Build a minimal `repo_root`-shaped tree covering `SOURCE_DIRS_FOR_HASH`, plus an irrelevant file."""
    for subdir in git_utils.SOURCE_DIRS_FOR_HASH:
        (tmp_path / subdir).mkdir()
        (tmp_path / subdir / "content.txt").write_text("original")
    (tmp_path / "leapfrog-validate").mkdir()
    (tmp_path / "leapfrog-validate" / "cli.py").write_text("original")
    return tmp_path


def test_hash_source_dirs_stable_when_content_unchanged(fake_source_tree):
    assert git_utils.hash_source_dirs(fake_source_tree) == git_utils.hash_source_dirs(fake_source_tree)


def test_hash_source_dirs_changes_when_hashed_dir_content_changes(fake_source_tree):
    before = git_utils.hash_source_dirs(fake_source_tree)
    (fake_source_tree / "leapfrogr" / "content.txt").write_text("modified")
    after = git_utils.hash_source_dirs(fake_source_tree)
    assert before != after


def test_hash_source_dirs_ignores_changes_outside_hashed_dirs(fake_source_tree):
    before = git_utils.hash_source_dirs(fake_source_tree)
    (fake_source_tree / "leapfrog-validate" / "cli.py").write_text("modified")
    after = git_utils.hash_source_dirs(fake_source_tree)
    assert before == after


def test_materialize_working_tree_copies_content_and_is_idempotent(fake_source_tree, tmp_path):
    cache_dir = tmp_path / "cache"
    first = git_utils.materialize_working_tree(fake_source_tree, cache_dir)
    assert (first / "leapfrogr" / "content.txt").read_text() == "original"

    second = git_utils.materialize_working_tree(fake_source_tree, cache_dir)
    assert first == second


def test_materialize_working_tree_uses_new_destination_when_source_changes(fake_source_tree, tmp_path):
    cache_dir = tmp_path / "cache"
    first = git_utils.materialize_working_tree(fake_source_tree, cache_dir)

    (fake_source_tree / "codegen" / "content.txt").write_text("modified")
    second = git_utils.materialize_working_tree(fake_source_tree, cache_dir)

    assert first != second
    assert (second / "codegen" / "content.txt").read_text() == "modified"


def test_prepare_source_dispatches_working_tree_sentinel(fake_source_tree, tmp_path):
    cache_dir = tmp_path / "cache"
    resolved = git_utils.prepare_source(fake_source_tree, cache_dir, git_utils.WORKING_TREE)
    assert resolved == git_utils.materialize_working_tree(fake_source_tree, cache_dir)


def test_prepare_source_dispatches_committed_ref(repo_root, tmp_path):
    resolved = git_utils.prepare_source(repo_root, tmp_path, "HEAD")
    sha = git_utils.resolve_ref(repo_root, "HEAD")
    assert resolved == tmp_path / "worktrees" / sha

    subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "remove", "--force", str(resolved)],
        check=True,
    )
