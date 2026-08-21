#!/usr/bin/env Rscript

usage <- "Process a PJNZ file into a params.h5 artifact.
Usage:
  build_params.R <r-library> <pjnz-path> <output-path>

Arguments:
  <r-library>    R library path leapfrogr was installed into.
  <pjnz-path>    Path to the PJNZ file to process.
  <output-path>  Where to write the params artifact.

Options:
  -h --help      Show this screen.
"

dat <- docopt::docopt(usage)
names(dat) <- gsub("-", "_", names(dat), fixed = TRUE)

.libPaths(c(dat$r_library, .libPaths()))

pars <- leapfrog::process_pjnz(dat$pjnz_path, extract_child_params = TRUE)
leapfrog::save_parameters(pars, dat$output_path)
