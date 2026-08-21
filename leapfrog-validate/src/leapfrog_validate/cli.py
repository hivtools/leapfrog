"""leapfrog-validate CLI.

Composable primitives, independently invokable: build-params, run, diff.
See `.scratch/leapfrog-validation/issues/15-walking-skeleton-single-indicator-diff.md`.
"""

from pathlib import Path
from typing import Annotated

import typer

from leapfrog_validate import build, git_utils, indicators, model_run, params
from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.diff import Verdict, diff_indicator
from leapfrog_validate.exclusions import exclusion_mask

app = typer.Typer(help="Compare leapfrog model output across git refs.")

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "leapfrog-validate"


def _prepare_ref(repo_root: Path, cache_dir: Path, ref: str) -> BuildWorkspace:
    sha = git_utils.resolve_ref(repo_root, ref)
    typer.echo(f"Resolved '{ref}' -> {sha}")
    worktree = git_utils.ensure_worktree(repo_root, sha, cache_dir)
    typer.echo(f"Building leapfrogr at {worktree} ...")
    return build.build_leapfrogr(worktree)


@app.callback()
def set_cache_dir(
    ctx: typer.Context,
    cache_dir: Annotated[
        Path,
        typer.Option(
            envvar="LEAPFROG_VALIDATE_CACHE_DIR",
            help="Where per-ref build workspaces (git worktrees, installed R libraries) are cached.",
        ),
    ] = DEFAULT_CACHE_DIR,
) -> None:
    """Stash --cache-dir and the current repo root for every subcommand to read."""
    ctx.obj = {"cache_dir": cache_dir, "repo_root": git_utils.find_repo_root()}


@app.command("build-params")
def build_params_cmd(
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help="Git ref or SHA to build leapfrogr at.")],
    pjnz: Annotated[Path, typer.Argument(exists=True, help="PJNZ file to process.")],
    output: Annotated[Path, typer.Option("--output", "-o", help="Where to write the params artifact.")] = Path(
        "params.h5"
    ),
) -> None:
    """Build leapfrogr at REF and process PJNZ into a params.h5 artifact."""
    workspace = _prepare_ref(ctx.obj["repo_root"], ctx.obj["cache_dir"], ref)
    params.build_params(workspace, pjnz, output)
    typer.echo(f"Wrote {output}")


@app.command("run")
def run_cmd(
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help="Git ref or SHA to build leapfrogr at.")],
    params_path: Annotated[
        Path, typer.Argument(exists=True, metavar="PARAMS", help="params.h5 to run the model against.")
    ],
    output: Annotated[Path, typer.Option("--output", "-o", help="Where to write the raw output artifact.")] = Path(
        "output.h5"
    ),
    configuration: Annotated[
        str,
        typer.Option(help="Model configuration to run, see leapfrogr::list_model_configurations()."),
    ] = "Spectrum",
) -> None:
    """Build leapfrogr at REF and run the model against PARAMS, producing output.h5."""
    workspace = _prepare_ref(ctx.obj["repo_root"], ctx.obj["cache_dir"], ref)
    model_run.run_model(workspace, params_path, output, configuration)
    typer.echo(f"Wrote {output}")


def _diff_one(name: str, a: Path, b: Path, pjnz: str | None) -> Verdict:
    spec = indicators.INDICATORS[name]
    arr_a = spec["extract"](a)
    arr_b = spec["extract"](b)
    exclude = exclusion_mask(arr_a.shape, spec["exclusions"], pjnz) if pjnz is not None else None
    return diff_indicator(arr_a, arr_b, name, spec["tolerance"], exclude=exclude)


@app.command("diff")
def diff_cmd(
    a: Annotated[Path, typer.Argument(exists=True)],
    b: Annotated[Path, typer.Argument(exists=True)],
    indicator: Annotated[
        str | None,
        typer.Option(help="Single indicator to compare. Defaults to all five blessed indicators."),
    ] = None,
    pjnz: Annotated[
        str | None,
        typer.Option(help="PJNZ identifier to match against each indicator's exclusion list."),
    ] = None,
) -> None:
    """Diff two output.h5 artifacts and print a pass/fail verdict per indicator.

    Fails overall (non-zero exit) if any indicator fails -- strict AND
    rollup, per ticket 07's Answer.
    """
    if indicator is not None and indicator not in indicators.INDICATORS:
        choices = ", ".join(sorted(indicators.INDICATORS))
        typer.echo(f"Invalid indicator '{indicator}'. Choose from: {choices}", err=True)
        raise typer.Exit(2)

    names = [indicator] if indicator is not None else sorted(indicators.INDICATORS)
    verdicts = [_diff_one(name, a, b, pjnz) for name in names]
    for verdict in verdicts:
        typer.echo(verdict.summary())

    raise typer.Exit(0 if all(v.passed for v in verdicts) else 1)


def main() -> None:
    """Entry point registered as the `leapfrog-validate` console script."""
    app()


if __name__ == "__main__":
    main()
