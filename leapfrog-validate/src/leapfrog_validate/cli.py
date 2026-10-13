"""leapfrog-validate CLI.

Composable primitives, independently invokable: build-params, run, diff.
See `.scratch/leapfrog-validation/issues/15-walking-skeleton-single-indicator-diff.md`.
"""

import functools
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Annotated

import typer

from leapfrog_validate import archive as archive_module
from leapfrog_validate import (
    archived_run,
    build,
    classify,
    git_utils,
    indicators,
    manifest,
    model_run,
    params,
    spectrum_archive,
)
from leapfrog_validate.archive import Archive
from leapfrog_validate.archived_run import RefIdentity
from leapfrog_validate.build import BuildWorkspace, LazyWorkspace
from leapfrog_validate.diff import Verdict, diff_indicator
from leapfrog_validate.exclusions import exclusion_mask

app = typer.Typer(help="Compare leapfrog model output across git refs.")


class CorpusError(RuntimeError):
    """Raised when a PJNZ corpus (local or Azure Blob) can't be safely resolved."""

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "leapfrog-validate"

REF_HELP = f"Git ref/SHA to build leapfrogr at, or '{git_utils.WORKING_TREE}' for your own uncommitted checkout."

ARCHIVE_ROOT_HELP = (
    "Orderly2 root that archives raw run outputs and Spectrum extracts (ticket 24). "
    "Unset: nothing is archived or reused. Needs R with the `orderly` package."
)
ARCHIVE_REMOTE_HELP = "Orderly location the archive pulls missing packets from and pushes new packets to."
ARCHIVE_REMOTE_PATH_HELP = "Directory to register --archive-remote at, as a path location, if it is not registered yet."

# Shared by this module's global options and `spectrum_track run`'s own.
ArchiveRootOption = Annotated[Path | None, typer.Option(envvar=archive_module.ENV_ROOT, help=ARCHIVE_ROOT_HELP)]
ArchiveRemoteOption = Annotated[str | None, typer.Option(envvar=archive_module.ENV_REMOTE, help=ARCHIVE_REMOTE_HELP)]
ArchiveRemotePathOption = Annotated[
    Path | None, typer.Option(envvar=archive_module.ENV_REMOTE_PATH, help=ARCHIVE_REMOTE_PATH_HELP)
]


def _ref_identity(repo_root: Path, ref: str) -> RefIdentity | None:
    """`ref` as given plus its resolved commit SHA; `None` for the uncommitted working tree (never archived)."""
    if ref == git_utils.WORKING_TREE:
        return None
    return RefIdentity(given=ref, sha=git_utils.resolve_ref(repo_root, ref))


def _workspace_for(repo_root: Path, cache_dir: Path, ref: str, *, archive: Archive | None) -> BuildWorkspace:
    """Build `ref` now, or -- with an archive -- only when something first needs it.

    With an archive configured every run is looked up before any compute,
    so a fully cached comparison never builds leapfrogr. Without one the
    build stays eager and up front, exactly as before ticket 24.
    """
    if archive is None:
        return _prepare_ref(repo_root, cache_dir, ref)
    return LazyWorkspace(lambda: _prepare_ref(repo_root, cache_dir, ref))


def _prepare_ref(repo_root: Path, cache_dir: Path, ref: str) -> BuildWorkspace:
    worktree = git_utils.prepare_source(repo_root, cache_dir, ref)
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
    archive_root: ArchiveRootOption = None,
    archive_remote: ArchiveRemoteOption = None,
    archive_remote_path: ArchiveRemotePathOption = None,
) -> None:
    """Stash --cache-dir, the repo root, and the (optional) run archive for every subcommand to read."""
    ctx.obj = {
        "cache_dir": cache_dir,
        "repo_root": git_utils.find_repo_root(),
        "archive": archive_module.archive_from_settings(archive_root, archive_remote, archive_remote_path),
    }


@app.command("build-params")
def build_params_cmd(
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help=REF_HELP)],
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
def run_cmd(  # noqa: PLR0913, PLR0917 - a CLI command's flat option surface; typer has no option-group dataclass
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help=REF_HELP)],
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
    pjnz: Annotated[
        Path | None,
        typer.Option(
            "--pjnz",
            exists=True,
            dir_okay=False,
            help="The PJNZ file PARAMS was built from. Names the archive key, so it is required "
            "when an archive is configured and ignored otherwise.",
        ),
    ] = None,
) -> None:
    """Build leapfrogr at REF and run the model against PARAMS, producing output.h5.

    With an archive configured (`--archive-root`), a packet already stored for
    the same PJNZ, resolved REF SHA, and configuration is reused instead of
    running the model, and a freshly computed output is archived.
    """
    archive = ctx.obj["archive"]
    if archive is not None and pjnz is None:
        typer.echo("--pjnz is required with an archive: it names the PJNZ that PARAMS came from.", err=True)
        raise typer.Exit(2)

    repo_root = ctx.obj["repo_root"]
    identity = _ref_identity(repo_root, ref) if archive is not None else None
    workspace = _workspace_for(
        repo_root, ctx.obj["cache_dir"], identity.sha if identity else ref, archive=archive
    )
    if archive is None:
        model_run.run_model(workspace, params_path, output, configuration)
    else:
        archived_run.obtain_output(
            archive=archive,
            ref=identity,
            pjnz=pjnz,
            pjnz_label=pjnz.name,
            output_path=output,
            configuration=configuration,
            compute=lambda: model_run.run_model(workspace, params_path, output, configuration),
            log=typer.echo,
        )
    typer.echo(f"Wrote {output}")


@app.command("extract")
def extract_cmd(
    ctx: typer.Context,
    pjnz: Annotated[Path, typer.Argument(exists=True, dir_okay=False, help="PJNZ file to read Spectrum modvars from.")],
    output: Annotated[Path, typer.Option("--output", "-o", help="Where to write the extract artifact.")] = Path(
        "extract.h5"
    ),
) -> None:
    """Read PJNZ's Spectrum modvars (no live Spectrum.exe) into an extract.h5 artifact.

    The artifact holds the raw modvars the blessed Spectrum indicators read,
    not indicators. With an archive configured (`--archive-root`), a packet
    already stored for the same PJNZ (file name + content hash; no git ref
    involved) is reused instead of running the importer, and a fresh
    extract is archived.
    """
    with tempfile.TemporaryDirectory() as tmp:
        modvars = spectrum_archive.obtain_modvars(
            archive=ctx.obj["archive"], pjnz=pjnz, pjnz_label=pjnz.name, work_dir=Path(tmp), log=typer.echo
        )
    tags = spectrum_archive.blessed_modvar_tags()
    spectrum_archive.write_extract_h5({tag: modvars[tag] for tag in tags}, output)
    typer.echo(f"Wrote {output}")


@app.command("classify")
def classify_cmd(
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help="Git ref or SHA to build leapfrogr at.")],
    pjnz: Annotated[Path, typer.Argument(exists=True, help="PJNZ file to classify.")],
    manifest_path: Annotated[
        Path | None,
        typer.Option(
            "--manifest", exists=True, help="JSON manifest of tags that can't be derived from file contents."
        ),
    ] = None,
) -> None:
    """Print PJNZ's derived shape/domain/manifest tags, one per line, sorted.

    Shape/manifest tags are checked before building leapfrogr at REF, so a
    bad PJNZ/manifest fails fast rather than after a multi-minute build.
    """
    manifest_data = manifest.load_manifest(manifest_path) if manifest_path is not None else {}
    tags = classify.shape_tags(pjnz)
    if manifest_data:
        tags |= manifest.manifest_tags(manifest_data, pjnz)

    workspace = _prepare_ref(ctx.obj["repo_root"], ctx.obj["cache_dir"], ref)
    tags |= classify.domain_tags(workspace, pjnz)

    for tag in sorted(tags):
        typer.echo(tag)


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

    Runs every indicator named in `indicators.INDICATORS` unconditionally,
    with no `Scope` (ticket 20) filtering -- unlike `compare`, this command
    operates on two already-produced `output.h5` artifacts with no PJNZ
    file to classify at all (`pjnz` here is just a caller-supplied string
    matched against exclusion entries, never resolved from a real file or
    corpus). Once a tag-scoped indicator exists, `diff` and `compare` can
    therefore disagree about whether it applies to a given PJNZ's output --
    a known, deliberate scope gap (`diff` would need a real PJNZ argument to
    classify from, which is a bigger change than this ticket's remit).
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


def _list_pjnz_files(root: Path) -> list[Path]:
    """Every `.PJNZ` file under `root`, recursive.

    Recursive (not just top-level `iterdir()`) because the real private
    corpus has subfolders (e.g. `ETH/`, see ticket 16's `infra/README.md`) --
    a flat `--pjnz-dir` test fixture gets the same result either way.
    """
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.upper() == ".PJNZ")


def _pjnz_label(pjnz: Path, corpus_root: Path) -> str:
    """`pjnz`'s path relative to `corpus_root`, POSIX-separated (e.g. `"ETH/foo.PJNZ"`).

    Equals `pjnz.name` for a flat corpus (today's only real case) -- this
    only differs once subfolders are involved, which is also exactly when a
    bare filename stops being a safe identifier (ticket 16's flagged
    same-basename-in-different-subfolders limitation).
    """
    return pjnz.relative_to(corpus_root).as_posix()


def _applicable_indicator_names(pjnz_tags: frozenset[str]) -> list[str]:
    """Return indicator names whose `Scope` (ticket 20) accepts `pjnz_tags`, sorted."""
    return sorted(name for name, spec in indicators.INDICATORS.items() if spec["scope"].applies_to(pjnz_tags))


@dataclass(frozen=True)
class _RefPair:
    """The two workspaces one `compare` run diffs against each other.

    The optional fields switch the run archive on (ticket 24): `archive` is
    where raw outputs are looked up and stored, and each `*_identity` is the
    side's ref plus resolved SHA (`None` for an uncommitted working tree,
    which is never archived). With all three left at their defaults every
    output is computed live, as before.
    """

    ref: BuildWorkspace
    candidate: BuildWorkspace
    archive: Archive | None = None
    ref_identity: RefIdentity | None = None
    candidate_identity: RefIdentity | None = None


def _build_and_run(
    workspace: BuildWorkspace, pjnz: Path, params_path: Path, output_path: Path, configuration: str
) -> None:
    """Process `pjnz`, then run the model on the result: the compute behind `archived_run.obtain_output`."""
    params.build_params(workspace, pjnz, params_path)
    model_run.run_model(workspace, params_path, output_path, configuration)


@dataclass(frozen=True)
class _ScopedPjnz:
    """One PJNZ file, already labeled (`_pjnz_label`) and scope-filtered to its applicable indicators."""

    path: Path
    label: str
    indicator_names: list[str]


def _compare_one_pjnz(
    workspaces: _RefPair,
    scoped: _ScopedPjnz,
    configuration: str,
    tmp_dir: Path,
    log: Callable[[str], None] = typer.echo,
) -> list[Verdict]:
    """Run build-params/run/diff for one PJNZ file, against both workspaces.

    Each side's `output.h5` comes from `archived_run.obtain_output`: reused
    from the archive when `workspaces.archive` has a packet at the exact
    key, computed (and archived) otherwise. The diff itself is always live.

    `scoped.indicator_names` is the already scope-filtered subset of
    `indicators.INDICATORS` applicable to this PJNZ (`compare_cmd` computes
    it once via `classify.classify` before calling this helper).
    `scoped.label` (see `_pjnz_label`) -- not `scoped.path.stem` -- seeds
    the tmp-file basenames and the exclusion-matching identifier, so two
    same-named files in different corpus subfolders don't collide on disk
    or in exclusion lookups; it collapses to the old `pjnz.stem` exactly
    for a flat corpus.
    """
    safe_base = scoped.label.removesuffix(scoped.path.suffix).replace("/", "__")
    output_ref = tmp_dir / f"{safe_base}-ref-output.h5"
    output_candidate = tmp_dir / f"{safe_base}-candidate-output.h5"
    sides = (
        ("ref", workspaces.ref, workspaces.ref_identity, output_ref),
        ("candidate", workspaces.candidate, workspaces.candidate_identity, output_candidate),
    )
    for side, workspace, identity, output_path in sides:
        params_path = tmp_dir / f"{safe_base}-{side}-params.h5"
        archived_run.obtain_output(
            archive=workspaces.archive,
            ref=identity,
            pjnz=scoped.path,
            pjnz_label=scoped.label,
            output_path=output_path,
            configuration=configuration,
            compute=functools.partial(_build_and_run, workspace, scoped.path, params_path, output_path, configuration),
            log=log,
        )

    return [_diff_one(name, output_ref, output_candidate, safe_base) for name in sorted(scoped.indicator_names)]


AZURE_CORPUS_PREFIX_DEFAULT = "2026 Estimates/Public Spectrum files"


def _azure_blob_service_client(account: str) -> "BlobServiceClient":  # noqa: F821 - forward ref, imported lazily below
    """Build a `BlobServiceClient` for `account`, authenticated via `DefaultAzureCredential`.

    `DefaultAzureCredential` tries, among other sources, an already
    `az login`'d CLI session (local/manual use) and, in CI once tickets
    21/22 wire up `azure/login@v2` with `permissions: id-token: write`, the
    GitHub-OIDC-federated `leapfrog-ci-reader` managed identity provisioned
    by ticket 16's `leapfrog-validate/infra/` -- no static secret either
    way. Imported lazily (`PLC0415` waived below) so importing this CLI
    module doesn't hard-require `azure-identity`/`azure-storage-blob` to be
    importable for callers who never touch `--azure-container`.
    """
    from azure.identity import DefaultAzureCredential  # noqa: PLC0415
    from azure.storage.blob import BlobServiceClient  # noqa: PLC0415

    return BlobServiceClient(
        account_url=f"https://{account}.blob.core.windows.net",
        credential=DefaultAzureCredential(),
    )


def _close_quietly(obj: object | None) -> None:
    """Best-effort `.close()` on `obj`, if it has one.

    Used for the Azure SDK client/credential, which should be closed when
    done with them rather than leaking open HTTP connection pools -- but
    `obj` is a test double (no `close()` at all) in most of this module's
    test suite, so this tolerates that rather than requiring every fake to
    implement one.
    """
    close = getattr(obj, "close", None)
    if callable(close):
        close()


def _download_azure_pjnz_corpus(
    blob_service_client: "BlobServiceClient",  # noqa: F821 - forward ref, see _azure_blob_service_client
    container: str,
    prefix: str,
    dest_dir: Path,
) -> list[Path]:
    """Download every `.PJNZ` blob under `prefix` in `container` into `dest_dir`.

    Preserves each blob's path relative to `prefix` (so the real corpus's
    `ETH/` subfolder, per ticket 16's `infra/README.md`, lands at
    `dest_dir/ETH/...`, not flattened) -- `_list_pjnz_files`'s recursive
    walk then finds it exactly like a local `--pjnz-dir` subfolder. Listing
    is always done fresh against the container, so a newly uploaded,
    correctly-tagged PJNZ is picked up automatically next run -- no code or
    config change (this ticket's third acceptance criterion).
    """
    container_client = blob_service_client.get_container_client(container)
    # An empty prefix means "no filter, match every blob" -- adding a
    # trailing slash to an empty string would instead match nothing, since
    # no real blob name starts with "/".
    prefix_dir = f"{prefix.rstrip('/')}/" if prefix else ""
    downloaded: list[Path] = []
    for blob in container_client.list_blobs(name_starts_with=prefix_dir):
        if not blob.name.upper().endswith(".PJNZ"):
            continue
        dest = dest_dir / _safe_relative_blob_path(blob.name, prefix_dir)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as fh:
            container_client.download_blob(blob.name).readinto(fh)
        downloaded.append(dest)
    return sorted(downloaded)


def _safe_relative_blob_path(blob_name: str, prefix_dir: str) -> PurePosixPath:
    """Validate and return the blob's path relative to `prefix_dir`, safe to join onto `dest_dir`.

    `dest_dir / tail` would otherwise either silently discard `dest_dir`
    (if `tail` is absolute -- e.g. a blob named with a doubled `//` right
    after the prefix) or escape it via a `..` segment. A blob name this
    malformed/malicious should never reach the corpus in practice (ticket
    16's upload path controls the layout), but a CLI that writes
    corpus-controlled bytes to disk must not trust it blindly either.
    """
    rel = PurePosixPath(blob_name[len(prefix_dir) :])
    if rel.is_absolute() or ".." in rel.parts:
        msg = f"Refusing to download blob with an unsafe relative path: {blob_name!r}"
        raise CorpusError(msg)
    return rel


def _resolve_corpus_files_core(
    pjnz_dir: Path | None,
    azure_container: str | None,
    azure_account: str | None,
    azure_prefix: str,
    tmp_path: Path,
) -> tuple[list[Path], Path]:
    """Resolve the PJNZ source (local dir or Azure Blob) to its files + corpus root.

    Raises `CorpusError` (never `typer.Exit`, unlike the thin `typer`-facing
    wrapper below) if the resolved corpus is empty or an unsafe blob path is
    hit -- a plain, `typer`-independent core so `report_regression.py`
    (ticket 21) can call it directly instead of duplicating this logic
    (extracted during that ticket's build after code review flagged the
    near-line-for-line duplicate). Reports the account/container/prefix
    rather than the Azure branch's ephemeral temp dir path in the
    empty-corpus message, since the latter means nothing to a reader once
    this process exits.
    """
    if azure_container is not None:
        corpus_root = tmp_path / "azure-corpus"
        corpus_root.mkdir()
        blob_service_client = _azure_blob_service_client(azure_account)
        try:
            pjnz_files = _download_azure_pjnz_corpus(blob_service_client, azure_container, azure_prefix, corpus_root)
        finally:
            # Belt-and-suspenders: close the client and the credential it
            # holds explicitly, rather than relying on either the SDK's own
            # internals or process exit to release open HTTP connection
            # pools -- matches azure-identity/azure-storage-blob's
            # documented context-manager pattern.
            _close_quietly(blob_service_client)
            _close_quietly(getattr(blob_service_client, "credential", None))
        corpus_description = f"Azure container '{azure_container}' (account '{azure_account}', prefix '{azure_prefix}')"
    else:
        corpus_root = pjnz_dir
        pjnz_files = _list_pjnz_files(corpus_root)
        corpus_description = str(corpus_root)

    if not pjnz_files:
        msg = f"No PJNZ files found in {corpus_description}"
        raise CorpusError(msg)
    return pjnz_files, corpus_root


def _resolve_corpus_files(
    pjnz_dir: Path | None,
    azure_container: str | None,
    azure_account: str | None,
    azure_prefix: str,
    tmp_path: Path,
) -> tuple[list[Path], Path]:
    """`typer`-facing wrapper around `_resolve_corpus_files_core`.

    Converts any `CorpusError` (a malformed/unsafe blob name, per ticket
    16's upload path controlling layout -- never expected in practice but
    not trusted blindly either; or an empty corpus) into a clean CLI error
    (`typer.Exit(2)`) rather than a raw traceback.
    """
    try:
        return _resolve_corpus_files_core(pjnz_dir, azure_container, azure_account, azure_prefix, tmp_path)
    except CorpusError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2) from e


@dataclass(frozen=True)
class _CompareRunContext:
    """Everything about one `compare` invocation that stays constant across every PJNZ in the loop."""

    workspaces: _RefPair
    corpus_root: Path
    manifest_data: dict[str, frozenset[str]]
    needs_tags: bool
    configuration: str
    tmp_path: Path


def _process_one_pjnz_in_compare(run_ctx: _CompareRunContext, pjnz: Path) -> tuple[str, bool]:
    """Classify, scope-filter, and compare one PJNZ; print as it goes; return `(label, passed)`.

    A `classify.ClassifyError` (e.g. the Goals-enabled `process_pjnz_ha`
    limitation `classify.py`'s own docstring documents) is caught here and
    reported as a clean per-file error rather than aborting the whole
    `compare` run and losing every other file's already-computed result.
    """
    label = _pjnz_label(pjnz, run_ctx.corpus_root)
    typer.echo(f"\n== {label} ==")
    try:
        pjnz_tags = (
            classify.classify(run_ctx.workspaces.ref, pjnz, run_ctx.manifest_data, corpus_root=run_ctx.corpus_root)
            if run_ctx.needs_tags
            else frozenset()
        )
    except classify.ClassifyError as e:
        typer.echo(f"  ERROR  could not classify: {e}", err=True)
        return label, False

    applicable = _applicable_indicator_names(pjnz_tags)
    skipped = sorted(set(indicators.INDICATORS) - set(applicable))
    if pjnz_tags:
        typer.echo(f"  tags: {', '.join(sorted(pjnz_tags))}")

    scoped = _ScopedPjnz(path=pjnz, label=label, indicator_names=applicable)
    verdicts = _compare_one_pjnz(run_ctx.workspaces, scoped, run_ctx.configuration, run_ctx.tmp_path)
    for verdict in verdicts:
        typer.echo(f"  {verdict.summary()}")
    for name in skipped:
        typer.echo(f"  SKIP  {name}: pjnz tags {sorted(pjnz_tags)!r} don't satisfy its scope")
    passed = all(v.passed for v in verdicts)
    typer.echo(f"  {label}: {'PASS' if passed else 'FAIL'}")
    return label, passed


@app.command("compare")
def compare_cmd(  # noqa: PLR0913, PLR0917 - a CLI command's flat option surface is inherently this wide;
    # typer has no native support for grouping options into one bound dataclass parameter.
    ctx: typer.Context,
    ref: Annotated[str, typer.Argument(help=REF_HELP)],
    candidate: Annotated[str, typer.Argument(help=REF_HELP)],
    pjnz_dir: Annotated[
        Path | None,
        typer.Option(
            "--pjnz-dir",
            exists=True,
            file_okay=False,
            help="Local directory of PJNZ files to compare across. Mutually exclusive with --azure-container.",
        ),
    ] = None,
    azure_container: Annotated[
        str | None,
        typer.Option(
            "--azure-container",
            help="Azure Blob container holding the private PJNZ corpus (ticket 16's infra/). "
            "Mutually exclusive with --pjnz-dir. Falls back to $AZURE_STORAGE_CONTAINER only if "
            "neither this nor --pjnz-dir is given at all.",
        ),
    ] = None,
    azure_account: Annotated[
        str | None,
        typer.Option(
            "--azure-account",
            help="Azure storage account name, used whenever the Azure source is selected either "
            "way (explicitly or via $AZURE_STORAGE_CONTAINER). Falls back to $AZURE_STORAGE_ACCOUNT.",
        ),
    ] = None,
    azure_prefix: Annotated[
        str,
        typer.Option(
            "--azure-prefix",
            help="Blob-name prefix the corpus lives under within the container.",
        ),
    ] = AZURE_CORPUS_PREFIX_DEFAULT,
    manifest_path: Annotated[
        Path | None,
        typer.Option(
            "--manifest", exists=True, help="JSON manifest of tags that can't be derived from file contents."
        ),
    ] = None,
    configuration: Annotated[
        str,
        typer.Option(help="Model configuration to run, see leapfrogr::list_model_configurations()."),
    ] = "Spectrum",
) -> None:
    """Run build-params/run/diff for every PJNZ in the corpus, comparing REF against CANDIDATE.

    The PJNZ source is either a local directory (`--pjnz-dir`) or the
    private Azure Blob corpus (`--azure-container`/`--azure-account`,
    ticket 16's `infra/`) -- exactly one of the two must be given.

    Each PJNZ's tags (`classify.classify`: shape + domain + optional
    `--manifest` tags) are checked against every indicator's `Scope`
    (ticket 20); an indicator whose scope the file doesn't match is skipped
    for that file alone, reported as a `SKIP` line rather than run. Tags are
    only computed at all if at least one registered indicator has a
    non-`ALL` scope, or if `--manifest` was explicitly given (so that flag
    isn't a silent no-op even against today's five blessed, all-`ALL`
    indicators) -- otherwise the five blessed indicators alone don't pay
    for a classify call that can't change their outcome.

    Tags are derived from REF's build only, not CANDIDATE's -- a deliberate
    choice (treats tags as a PJNZ property, avoids doubling the classify
    cost per file), but one with a real edge case: if the classification
    logic itself changed between REF and CANDIDATE (e.g. a PR changing how
    PMTCT presence is detected), eligibility for a tag-scoped indicator is
    decided purely by REF's answer for that comparison.

    Prints a per-indicator verdict per PJNZ file, then a per-file PASS/FAIL
    summary line. Exits non-zero if any file fails any applicable indicator.
    """
    # Deliberately *not* done via typer's `envvar=` on the options themselves:
    # that would populate `azure_container`/`azure_account` from the
    # environment unconditionally, so an explicit `--pjnz-dir` could be
    # silently rejected by the mutual-exclusivity check below just because
    # AZURE_STORAGE_CONTAINER/AZURE_STORAGE_ACCOUNT happen to be exported in
    # the caller's shell/CI job (e.g. for some unrelated step) -- a real,
    # empirically-reproduced bug caught in review. Only consult the env var
    # as a corpus-*source* fallback when the CLI itself chose neither.
    if pjnz_dir is None and azure_container is None:
        azure_container = os.environ.get("AZURE_STORAGE_CONTAINER")
    if azure_container is not None:
        azure_account = azure_account or os.environ.get("AZURE_STORAGE_ACCOUNT")

    if (pjnz_dir is not None) == (azure_container is not None):
        typer.echo("Specify exactly one of --pjnz-dir or --azure-container as the PJNZ source.", err=True)
        raise typer.Exit(2)
    if azure_container is not None and not azure_account:
        typer.echo("--azure-account is required together with --azure-container.", err=True)
        raise typer.Exit(2)

    manifest_data = manifest.load_manifest(manifest_path) if manifest_path is not None else {}
    needs_tags = manifest_path is not None or any(
        spec["scope"].tags is not None for spec in indicators.INDICATORS.values()
    )

    file_results: dict[str, bool] = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pjnz_files, corpus_root = _resolve_corpus_files(
            pjnz_dir, azure_container, azure_account, azure_prefix, tmp_path
        )

        # Corpus resolved and non-empty before paying for the (multi-minute)
        # leapfrogr build, same fail-fast ordering as the single-directory
        # case this replaces.
        # With an archive, each committed ref is resolved to its SHA once and
        # that SHA is what gets built, so the archive key and the build can
        # never disagree even if a moving branch advances mid-run.
        repo_root, cache_dir, archive = ctx.obj["repo_root"], ctx.obj["cache_dir"], ctx.obj["archive"]
        ref_identity = _ref_identity(repo_root, ref) if archive is not None else None
        candidate_identity = _ref_identity(repo_root, candidate) if archive is not None else None
        run_ctx = _CompareRunContext(
            workspaces=_RefPair(
                ref=_workspace_for(repo_root, cache_dir, ref_identity.sha if ref_identity else ref, archive=archive),
                candidate=_workspace_for(
                    repo_root, cache_dir, candidate_identity.sha if candidate_identity else candidate, archive=archive
                ),
                archive=archive,
                ref_identity=ref_identity,
                candidate_identity=candidate_identity,
            ),
            corpus_root=corpus_root,
            manifest_data=manifest_data,
            needs_tags=needs_tags,
            configuration=configuration,
            tmp_path=tmp_path,
        )

        for pjnz in pjnz_files:
            label, passed = _process_one_pjnz_in_compare(run_ctx, pjnz)
            file_results[label] = passed

    typer.echo("\n== Summary ==")
    for label, passed in file_results.items():
        typer.echo(f"  {'PASS' if passed else 'FAIL'}  {label}")

    raise typer.Exit(0 if all(file_results.values()) else 1)


def main() -> None:
    """Entry point registered as the `leapfrog-validate` console script."""
    app()


if __name__ == "__main__":
    main()
