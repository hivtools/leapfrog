"""`LazyWorkspace`: a `BuildWorkspace` that only builds when first used (ticket 24).

An archive hit never touches the workspace, so a fully cached run must not
pay for the multi-minute leapfrogr build.
"""

from pathlib import Path

from leapfrog_validate.build import BuildWorkspace, LazyWorkspace


def _counting_prepare():
    calls = []

    def prepare() -> BuildWorkspace:
        calls.append(1)
        return BuildWorkspace(worktree=Path("/w"), r_library=Path("/w/lib"))

    return prepare, calls


def test_creating_one_does_not_build():
    prepare, calls = _counting_prepare()

    LazyWorkspace(prepare)

    assert calls == []


def test_first_use_builds_and_later_uses_reuse_it():
    prepare, calls = _counting_prepare()
    lazy = LazyWorkspace(prepare)

    assert lazy.worktree == Path("/w")
    assert lazy.r_library == Path("/w/lib")
    assert calls == [1]
