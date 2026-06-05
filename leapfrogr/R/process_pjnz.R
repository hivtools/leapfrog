#' Prepare inputs from Spectrum PJNZ
#'
#' @param pjnz path to PJNZ file
#' @param use_coarse_age_groups use the coarse age stratification
#' @param extract_child_params If TRUE, then child parameters required
#'  to run the child model will be extracted. If FALSE, only adult parameters
#'  will be extracted from the PJNZ.
#' @param bypass_adult produce parameters that will bypass the adult
#'  model when running the child model variant
#'
#' @return list of input parameters
#'
#' @examples
#' pjnz <- system.file(
#'   "pjnz/bwa_aim-adult-art-no-special-elig_v6.13_2022-04-18.PJNZ",
#'   package = "leapfrog")
#' parameters <- process_pjnz(pjnz)
#'
#' @export
process_pjnz <- function(
    pjnz,
    use_coarse_age_groups = FALSE,
    extract_child_params = FALSE,
    bypass_adult = FALSE
) {
  dat <- pjnz::read_dp(pjnz, include_raw = TRUE)
  dim_vars <- dat$dim_vars

  pars <- lapply(dat$data, `[[`, "data")

  pars <- process_pjnz_dp(dat, pars, dim_vars)
  pars <- process_pjnz_ha(dat, pars, dim_vars, use_coarse_age_groups)
  if (extract_child_params || bypass_adult) {
    pars <- process_pjnz_hc(dat, pars, dim_vars, use_coarse_age_groups, bypass_adult)
  }
  pars
}
