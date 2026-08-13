"""process_pjnz, run at a given ref -> a params.h5-equivalent artifact."""

from pathlib import Path

from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.subprocess_utils import run_checked

_SCRIPT = Path(__file__).parent / "r_scripts" / "build_params.R"


class ParamsBuildError(RuntimeError):
    pass


def build_params(workspace: BuildWorkspace, pjnz: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    run_checked(
        ["Rscript", str(_SCRIPT), str(workspace.r_library), str(pjnz), str(output)],
        cwd=workspace.worktree,
        error_cls=ParamsBuildError,
        error_context="build-params",
    )
