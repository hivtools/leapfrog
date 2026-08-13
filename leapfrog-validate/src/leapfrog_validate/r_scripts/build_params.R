#!/usr/bin/env Rscript
# Args: <r_library> <pjnz_path> <output_path>
args <- commandArgs(trailingOnly = TRUE)
r_library <- args[[1]]
pjnz_path <- args[[2]]
output_path <- args[[3]]

.libPaths(c(r_library, .libPaths()))
library(leapfrog)

pars <- process_pjnz(pjnz_path, extract_child_params = TRUE)
save_parameters(pars, output_path)
