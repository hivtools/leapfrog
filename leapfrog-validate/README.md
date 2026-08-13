# leapfrog-validate

Compare leapfrog model output across git refs, and (eventually) against
Spectrum. See `.scratch/leapfrog-validation/PRD.md` for the full design;
this package currently implements the walking skeleton from
`.scratch/leapfrog-validation/issues/15-walking-skeleton-single-indicator-diff.md`.

## Usage

```sh
uv run leapfrog-validate build-params <ref> <pjnz> -o params.h5
uv run leapfrog-validate run <ref> params.h5 -o output.h5
uv run leapfrog-validate diff output-a.h5 output-b.h5
```

Each command independently builds `leapfrogr` (and regenerates the C++
headers it depends on) at the given git ref, in an isolated git worktree
cached under `--cache-dir` (default `~/.cache/leapfrog-validate`). `<ref>`
must be a committed ref or SHA -- uncommitted working-tree support is a
separate, later ticket.

`diff` extracts an indicator (`total_population` by default) from two
`output.h5` artifacts and applies a hybrid `atol + rtol*|ref|` per-cell
tolerance, printing a pass/fail verdict and exiting non-zero on failure.
