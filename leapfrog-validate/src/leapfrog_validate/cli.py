"""leapfrog-validate CLI.

Composable primitives, independently invokable: build-params, run, diff.
See `.scratch/leapfrog-validation/issues/15-walking-skeleton-single-indicator-diff.md`.
"""

import sys
from pathlib import Path

import click

from leapfrog_validate import build, git_utils, indicators, model_run, params
from leapfrog_validate.build import BuildWorkspace
from leapfrog_validate.diff import diff_indicator


def _prepare_ref(repo_root: Path, cache_dir: Path, ref: str) -> BuildWorkspace:
    sha = git_utils.resolve_ref(repo_root, ref)
    click.echo(f"Resolved '{ref}' -> {sha}")
    worktree = git_utils.ensure_worktree(repo_root, sha, cache_dir)
    click.echo(f"Building leapfrogr at {worktree} ...")
    return build.build_leapfrogr(worktree)


@click.group()
@click.option(
    "--cache-dir",
    type=click.Path(path_type=Path),
    default=Path.home() / ".cache" / "leapfrog-validate",
    show_default=True,
    envvar="LEAPFROG_VALIDATE_CACHE_DIR",
    help="Where per-ref build workspaces (git worktrees, installed R libraries) are cached.",
)
@click.pass_context
def main(ctx: click.Context, cache_dir: Path) -> None:
    """Compare leapfrog model output across git refs."""
    ctx.ensure_object(dict)
    ctx.obj["cache_dir"] = cache_dir
    ctx.obj["repo_root"] = git_utils.find_repo_root()


@main.command("build-params")
@click.argument("ref")
@click.argument("pjnz", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("params.h5"),
    show_default=True,
)
@click.pass_context
def build_params_cmd(ctx: click.Context, ref: str, pjnz: Path, output: Path) -> None:
    """Build leapfrogr at REF and process PJNZ into a params.h5 artifact."""
    workspace = _prepare_ref(ctx.obj["repo_root"], ctx.obj["cache_dir"], ref)
    params.build_params(workspace, pjnz, output)
    click.echo(f"Wrote {output}")


@main.command("run")
@click.argument("ref")
@click.argument("params_path", metavar="PARAMS", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output.h5"),
    show_default=True,
)
@click.option(
    "--configuration",
    default="Spectrum",
    show_default=True,
    help="Model configuration to run, see leapfrogr::list_model_configurations().",
)
@click.pass_context
def run_cmd(ctx: click.Context, ref: str, params_path: Path, output: Path, configuration: str) -> None:
    """Build leapfrogr at REF and run the model against PARAMS, producing output.h5."""
    workspace = _prepare_ref(ctx.obj["repo_root"], ctx.obj["cache_dir"], ref)
    model_run.run_model(workspace, params_path, output, configuration)
    click.echo(f"Wrote {output}")


@main.command("diff")
@click.argument("a", type=click.Path(exists=True, path_type=Path))
@click.argument("b", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--indicator",
    "indicator_name",
    default="total_population",
    show_default=True,
    type=click.Choice(sorted(indicators.INDICATORS)),
)
def diff_cmd(a: Path, b: Path, indicator_name: str) -> None:
    """Diff two output.h5 artifacts on --indicator and print a pass/fail verdict."""
    spec = indicators.INDICATORS[indicator_name]
    arr_a = spec["extract"](a)
    arr_b = spec["extract"](b)
    verdict = diff_indicator(arr_a, arr_b, indicator_name, spec["atol"], spec["rtol"])
    click.echo(verdict.summary())
    sys.exit(0 if verdict.passed else 1)
