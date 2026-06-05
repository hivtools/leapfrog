#!/usr/bin/env Rscript

# Sets LEAPFROG_INCLUDE in the user's .Renviron so that configure can locate
# leapfrog-core headers during devtools::install().
#
# Run once after cloning the repo:
#   Rscript leapfrogr/scripts/setup_dev_env.R
#
# Or from within the leapfrogr R project:
#   source("scripts/setup_dev_env.R")

pkg_root <- here::here()
core_include <- normalizePath(
  file.path(pkg_root, "../leapfrog-core/include"),
  mustWork = TRUE
)

message(sprintf("Found leapfrog-core headers at: %s", core_include))

renviron_path <- Sys.getenv("R_ENVIRON_USER",
                            unset = path.expand("~/.Renviron"))

# Read existing content, removing any previous LEAPFROG_INCLUDE entry.
existing <- if (file.exists(renviron_path)) {
  readLines(renviron_path, warn = FALSE)
} else {
  character(0)
}
existing <- existing[!grepl("^LEAPFROG_INCLUDE\\s*=", existing)]

writeLines(
  c(existing, sprintf('LEAPFROG_INCLUDE="%s"', core_include)),
  renviron_path
)

message(sprintf("Written LEAPFROG_INCLUDE to %s", renviron_path))
message("Restart R for the change to take effect in new sessions")
