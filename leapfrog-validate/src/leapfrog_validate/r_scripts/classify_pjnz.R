#!/usr/bin/env Rscript

usage <- "Derive domain tags for a PJNZ from its input parameters.

Imports the PJNZ via leapfrog::process_pjnz() and checks whether the
PMTCT/cotrimoxazole input arrays are all-zero -- a PJNZ that doesn't use
PMTCT/cotrim still carries the input variable, just zeroed out, so this
can't be read from the zip's file listing alone (see classify.py).

Prints one `key=TRUE` or `key=FALSE` line per tag to stdout.

Usage:
  classify_pjnz.R <r-library> <pjnz-path>

Arguments:
  <r-library>    R library path leapfrogr was installed into.
  <pjnz-path>    Path to the PJNZ file to classify.

Options:
  -h --help      Show this screen.
"

dat <- docopt::docopt(usage)
names(dat) <- gsub("-", "_", names(dat), fixed = TRUE)

.libPaths(c(dat$r_library, .libPaths()))

pars <- leapfrog::process_pjnz(dat$pjnz_path, extract_child_params = TRUE)

# NA-scrubs like prepare_pmtct() already does for PMTCT (process_pjnz_hc.R) --
# cotrim_val gets no equivalent scrub upstream, so without this an NA cell
# would make `all(x == 0)` evaluate to NA and silently vanish from the
# TRUE/FALSE-only parser downstream (classify.py's _parse_domain_tags_output).
# NULL/zero-length is treated as a hard error, not a guess: an empty array
# here signals a shape process_pjnz() doesn't produce, not "unused".
has_nonzero_input <- function(x, name) {
  if (is.null(x) || length(x) == 0) {
    stop(sprintf("expected a non-empty array for '%s', got %s", name, if (is.null(x)) "NULL" else "zero-length"))
  }
  x[is.na(x)] <- 0
  any(x != 0)
}

cat(sprintf("has_pmtct=%s\n", has_nonzero_input(pars$PMTCT, "PMTCT")))
cat(sprintf("has_cotrim=%s\n", has_nonzero_input(pars$cotrim_val, "cotrim_val")))
