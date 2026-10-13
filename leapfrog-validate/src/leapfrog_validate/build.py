"""Build leapfrogr (and the leapfrog-core headers it depends on) at a ref.

Fresh checkout + codegen + compile every time a new sha shows up, cached
behind an install marker per worktree so re-running against an unchanged
ref is cheap.
"""

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from leapfrog_validate.subprocess_utils import run_checked


class BuildError(RuntimeError):
    """Raised when generating C++ headers or installing leapfrogr fails."""


@dataclass(frozen=True)
class BuildWorkspace:
    """A checked-out ref with leapfrogr installed, ready to drive via Rscript."""

    worktree: Path
    r_library: Path


class LazyWorkspace:
    """A `BuildWorkspace` stand-in that runs `prepare` on first use, not on creation.

    Quacks like `BuildWorkspace` (`worktree`, `r_library`), so `params`,
    `model_run`, and `classify` accept it unchanged. Exists for ticket 24's
    archive: a cache hit never touches the workspace, so a fully cached run
    never pays for checkout + codegen + the leapfrogr compile.
    """

    def __init__(self, prepare: Callable[[], BuildWorkspace]) -> None:
        """Remember `prepare`; call nothing yet."""
        self._prepare = prepare
        self._workspace: BuildWorkspace | None = None

    def _get(self) -> BuildWorkspace:
        if self._workspace is None:
            self._workspace = self._prepare()
        return self._workspace

    @property
    def worktree(self) -> Path:
        """The checked-out source tree (builds on first access)."""
        return self._get().worktree

    @property
    def r_library(self) -> Path:
        """The R library leapfrogr was installed into (builds on first access)."""
        return self._get().r_library


def build_leapfrogr(worktree: Path) -> BuildWorkspace:
    """Generate C++ headers and install the leapfrogr R package from `worktree`."""
    r_library = worktree / ".leapfrog-validate" / "r-library"
    marker = r_library / ".install-complete"
    if marker.exists():
        return BuildWorkspace(worktree, r_library)

    r_library.mkdir(parents=True, exist_ok=True)

    run_checked(
        ["uv", "run", "src/main.py"],
        cwd=worktree / "codegen",
        error_cls=BuildError,
        error_context="codegen (generating C++ headers)",
    )

    env = os.environ.copy()
    env["LEAPFROG_INCLUDE"] = str(worktree / "leapfrog-core" / "include")
    # BASH_ENV, if set, gets re-sourced by every nested bash invocation R's
    # build machinery spawns (configure, Makevars, etc.) -- and if whatever
    # it sources re-exports LEAPFROG_INCLUDE, that silently overrides the
    # worktree-correct value set above, building against the wrong ref's
    # headers with no error. Drop it so our explicit value always wins.
    env.pop("BASH_ENV", None)
    run_checked(
        ["R", "CMD", "INSTALL", f"--library={r_library}", "."],
        cwd=worktree / "leapfrogr",
        error_cls=BuildError,
        env=env,
        error_context="R CMD INSTALL leapfrogr",
    )

    marker.touch()
    return BuildWorkspace(worktree, r_library)
