bwa_pjnz <- system_file(
  "pjnz/bwa_aim-adult-art-no-special-elig_v6.13_2022-04-18.PJNZ"
)

bwa_pmtct_pjnz <- system_file(
  "pjnz/bwa_aim-no-special-elig-numpmtct.PJNZ"
)

test_that("process_pjnz includes all required parameters", {
  pars <- process_pjnz(bwa_pjnz)

  ## DP
  expect_true(all(c("basepop", "Sx", "netmigr_adj", "asfr", "tfr",
                    "births_sex_prop", "projection_period",
                    "projection_start_year") %in% names(pars)))

  ## HIV adult
  expect_true(all(c("incidinput", "incrr_age", "incrr_sex",
                    "cd4_mort", "cd4_prog", "cd4_initdist",
                    "art_mort", "artmx_timerr", "artcd4elig_idx",
                    "art_dropout_rate", "art15plus_num", "art15plus_isperc",
                    "scale_cd4_mort", "incidence_model_choice") %in% names(pars)))

  ## Parameter dimensions are correct
  proj_years <- length(pars$tfr)
  expect_equal(dim(pars$basepop), c(81, 2, proj_years), ignore_attr = TRUE)
  expect_equal(dim(pars$cd4_mort), c(7, 66, 2), ignore_attr = TRUE)
  expect_equal(dim(pars$artmx_timerr),      c(3, proj_years),   ignore_attr = TRUE)

  ## DP params are in valid ranges
  expect_true(all(pars$Sx >= 0 & pars$Sx <= 1))
  expect_true(all(pars$basepop > 0))
  expect_true(all(pars$asfr >= 0))
  expect_true(all(pars$tfr > 0))
  # male + female birth proportions sum to 1 each year
  expect_equal(colSums(pars$births_sex_prop), rep(1, ncol(pars$births_sex_prop)),
               tolerance = 1e-10, ignore_attr = TRUE)
  expect_true(pars$projection_period %in% c("calendar", "midyear"))

  ## HIV adult params are in valid ranges
  expect_true(all(pars$incidinput >= 0 & pars$incidinput <= 1))
  expect_true(all(pars$incrr_age >= 0))
  expect_true(all(pars$incrr_sex > 0))
  # CD4 initial distribution sums to 1 over stages for each age/sex
  cd4_col_sums <- apply(pars$cd4_initdist, 2:3, sum)
  expect_equal(cd4_col_sums, matrix(1, 66, 2), tolerance = 1e-6, ignore_attr = TRUE)
  expect_true(all(pars$art_dropout_rate >= 0))
  # ART eligibility index must be within valid CD4 stage range (1-7)
  expect_true(all(pars$artcd4elig_idx >= 1L & pars$artcd4elig_idx <= 7L))
  expect_true(pars$scale_cd4_mort %in% c(0L, 1L))
})

test_that("process_pjnz use_coarse_age_groups changes HIV age stratification dimensions", {
  pars_full   <- process_pjnz(bwa_pjnz, use_coarse_age_groups = FALSE)
  pars_coarse <- process_pjnz(bwa_pjnz, use_coarse_age_groups = TRUE)

  expect_equal(dim(pars_full$cd4_mort),   c(7, 66, 2), ignore_attr = TRUE)
  expect_equal(dim(pars_coarse$cd4_mort), c(7,  9, 2), ignore_attr = TRUE)

  expect_equal(dim(pars_full$art_mort),   c(3, 7, 66, 2), ignore_attr = TRUE)
  expect_equal(dim(pars_coarse$art_mort), c(3, 7,  9, 2), ignore_attr = TRUE)

  # Demographic parameters are unaffected by age stratification choice
  expect_equal(dim(pars_full$basepop), dim(pars_coarse$basepop))
  expect_equal(dim(pars_full$Sx),      dim(pars_coarse$Sx))
})

test_that("process_pjnz extract_child_params adds child-specific parameters", {
  pars_adult <- process_pjnz(bwa_pmtct_pjnz)
  pars_child <- process_pjnz(bwa_pmtct_pjnz, extract_child_params = TRUE)

  child_pars <- c("hc_nosocomial_infections_by_age", "hc1_cd4_dist", "hc1_cd4_mort", 
                  "hc2_cd4_mort", "hc1_cd4_prog", "hc2_cd4_prog",
                  "ctx_val", "PMTCT", "vertical_transmission_rate")
  expect_true(all(child_pars %in% names(pars_child)))
  expect_false(any(child_pars %in% names(pars_adult)))

  # Adult parameters still present
  expect_true(all(c("basepop", "Sx", "cd4_mort") %in% names(pars_child)))
})

test_that("process_pjnz converts non-age stratified nosocomial infections to age stratified", {
  raw_dp <- pjnz::read_dp(bwa_pmtct_pjnz, include_raw = TRUE)
  raw_dp$data$nosocomial_infections <- list(
    data = rep(1, dim(raw_dp$data$nosocomial_infections_by_age$data)[2]),
    tag = "NoscomialInfections MV"
  )
  raw_dp$data$nosocomial_infections_by_age <- NULL

  with_mocked_bindings(
    pars_child <- process_pjnz(bwa_pmtct_pjnz, extract_child_params = TRUE),
    read_dp = function(...) raw_dp,
    .package = "pjnz"
  )

  expect_true(all(pars_child$hc_nosocomial_infections_by_age[1, ] == 1))
  expect_true(all(pars_child$hc_nosocomial_infections_by_age[2:15, ] == 0))
})
