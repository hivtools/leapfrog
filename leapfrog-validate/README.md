# leapfrog-validate

Compare leapfrog model output across git refs, and (eventually) against
Spectrum. See `.scratch/leapfrog-validation/PRD.md` for the full design;
this package currently implements the walking skeleton
(`.scratch/leapfrog-validation/issues/15-walking-skeleton-single-indicator-diff.md`)
plus the full five-indicator registry and exclusion mechanism
(`.scratch/leapfrog-validation/issues/17-full-indicator-registry-tolerance-rollup.md`).

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

`diff` applies a hybrid `atol + rtol*|ref|` per-cell tolerance (strict-max
rollup: any single over-tolerance cell fails that indicator) and, by
default, checks all five blessed indicators against two `output.h5`
artifacts -- `total_population`, `hiv_population`, `treatment_population`,
`aids_deaths_single_age`, `aids_deaths_on_treatment` -- printing one
pass/fail line per indicator and exiting non-zero if any of them fail.
Pass `--indicator <name>` to check just one.

`treatment_population` and `aids_deaths_on_treatment` have no single
leapfrog output array; they're reconstructed by summing the adult and
pediatric ART-population/ART-death arrays over CD4 stage and treatment
duration and concatenating the three age domains (see
`leapfrog_validate.indicators`).

### Excluding a known, explained discrepancy

Pass `--pjnz <identifier>` to have `diff` also check each indicator's
exclusion list (`leapfrog_validate.exclusions.Exclusion`) for entries
scoped to that PJNZ, carving out the matching (year, sex, age) cells from
the pass/fail rollup -- visible in the summary line as `N excluded` --
without loosening tolerance for any other PJNZ. Every `Exclusion` requires
both a `reason` and a `link` to the underlying explanation; constructing
one without either raises `ValueError`.
