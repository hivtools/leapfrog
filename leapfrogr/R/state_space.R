#' Run leapfrog model fit
#'
#' @param configuration The model configuration to run, see
#'   [list_model_configurations()] for available configurations
#'
#' @return The state space for this model configuration.
#' @examples
#' s <- get_state_space("HivCoarseAgeStratification")
#' @export
get_state_space <- function(configuration = "HivFullAgeStratification") {
  get_leapfrog_ss(configuration)
}
