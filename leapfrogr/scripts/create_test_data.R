#!/usr/bin/env Rscript
# Creates HDF5 parameter files used by leapfrogr tests.
# Run from the root of the leapfrogr package:
#   Rscript scripts/create_test_data.R

devtools::load_all(".")

pkg_root <- here::here()
test_data_dir <- file.path(pkg_root, "tests", "testthat", "testdata")

bwa_pjnz <- system.file(
  "pjnz/bwa_aim-adult-art-no-special-elig_v6.13_2022-04-18.PJNZ",
  package = "leapfrog"
)

bwa_pmtct_pjnz <- system.file(
  "pjnz/bwa_aim-no-special-elig-numpmtct.PJNZ",
  package = "leapfrog"
)

message("Creating adult_parms_full.h5 ...")
pars_adult_full <- process_pjnz(bwa_pjnz)
save_parameters(pars_adult_full, file.path(test_data_dir, "adult_parms_full.h5"))

message("Creating adult_parms_coarse.h5 ...")
pars_adult_coarse <- process_pjnz(bwa_pjnz, use_coarse_age_groups = TRUE)
save_parameters(pars_adult_coarse, file.path(test_data_dir, "adult_parms_coarse.h5"))

message("Creating child_parms_full.h5 ...")
pars_child_full <- process_pjnz(bwa_pmtct_pjnz, extract_child_params = TRUE)
save_parameters(pars_child_full, file.path(test_data_dir, "child_parms_full.h5"))

message("Creating child_parms_coarse.h5 ...")
pars_child_coarse <- process_pjnz(
  bwa_pmtct_pjnz,
  use_coarse_age_groups = TRUE,
  extract_child_params = TRUE
)
save_parameters(pars_child_coarse, file.path(test_data_dir, "child_parms_coarse.h5"))

message("Done. Test data files written to ", test_data_dir)
