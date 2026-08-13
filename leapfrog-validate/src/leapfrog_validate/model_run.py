"""run_model at a given ref -> the full raw output.h5 artifact."""

from pathlib import Path

from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.subprocess_utils import run_checked

_SCRIPT = Path(__file__).parent / "r_scripts" / "run_model.R"


class ModelRunError(RuntimeError):
    pass


def run_model(workspace: BuildWorkspace, params: Path, output: Path, configuration: str) -> None:
    # Resolve to absolute before handing off: the Rscript subprocess runs
    # with cwd=workspace.worktree (below), not the caller's directory, so a
    # relative path here would land inside the cached build workspace
    # instead of where the user actually pointed it.
    params = params.resolve()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    run_checked(
        ["Rscript", str(_SCRIPT), str(workspace.r_library), str(params), str(output), configuration],
        cwd=workspace.worktree,
        error_cls=ModelRunError,
        error_context="run",
    )
