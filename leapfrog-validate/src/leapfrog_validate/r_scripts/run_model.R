#!/usr/bin/env Rscript

usage <- "Run the leapfrog model against a params.h5 artifact.
Usage:
  run_model.R <r-library> <params-path> <output-path> <configuration>

Arguments:
  <r-library>      R library path leapfrogr was installed into.
  <params-path>    Path to the params.h5 artifact to run.
  <output-path>    Where to write the raw output artifact.
  <configuration>  Model configuration to run, see leapfrogr::list_model_configurations().

Options:
  -h --help        Show this screen.
"

dat <- docopt::docopt(usage)
names(dat) <- gsub("-", "_", names(dat), fixed = TRUE)

.libPaths(c(dat$r_library, .libPaths()))

parameters <- leapfrog::read_parameters(dat$params_path)
out <- leapfrog::run_model(parameters, configuration = dat$configuration)
leapfrog:::save_hdf5_file(out, dat$output_path)
