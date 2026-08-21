"""Build leapfrogr (and the leapfrog-core headers it depends on) at a ref.

Fresh checkout + codegen + compile every time a new sha shows up, cached
behind an install marker per worktree so re-running against an unchanged
ref is cheap.
"""

import os
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
