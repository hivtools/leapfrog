#!/usr/bin/env Rscript
# Args: <r_library> <params_path> <output_path> <configuration>
args <- commandArgs(trailingOnly = TRUE)
r_library <- args[[1]]
params_path <- args[[2]]
output_path <- args[[3]]
configuration <- args[[4]]

.libPaths(c(r_library, .libPaths()))
library(leapfrog)

parameters <- read_parameters(params_path)
out <- run_model(parameters, configuration = configuration)
leapfrog:::save_hdf5_file(out, output_path)
