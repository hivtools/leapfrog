#!/usr/bin/env Rscript

usage <- "Fetch from, or store into, a leapfrog-validate Orderly archive.

The archive is an Orderly root. The report sources (src/<report>/<report>.R)
ship with leapfrog-validate and are copied into the root on every call, so
a root never goes stale.

`fetch` looks for the latest packet of <report> whose parameters equal every
key in <key-json>. On a hit it copies <artefact> to <dest> and prints HIT.
On a miss it prints MISS and copies nothing.

`store` runs <report> with the keys in <key-json> plus the keys in
<extra-json> as parameters, hands <source> to the report, and (when a
remote is given) pushes the new packet to that remote.

Usage:
  archive.R fetch <project> <root> <report> <key-json> <artefact> <dest> [--remote=<name>] [--remote-path=<dir>]
  archive.R store <project> <root> <report> <key-json> <extra-json> <source> [--remote=<name>] [--remote-path=<dir>]

Arguments:
  <project>      Directory holding orderly_config.yml and src/ (the shipped report sources).
  <root>         The Orderly root to use as the local archive.
  <report>       Report name, for example leapfrog_run.
  <key-json>     JSON object of string parameters forming the exact lookup key.
  <extra-json>   JSON object of further string parameters stored on the packet.
  <artefact>     Artefact file name inside the packet.
  <dest>         Where to copy the artefact to.
  <source>       File to archive.

Options:
  --remote=<name>       Orderly location to pull from and push to.
  --remote-path=<dir>   Register <name> as a path location at <dir> if it is not registered yet.
  -h --help             Show this screen.
"

dat <- docopt::docopt(usage)

ensure_root <- function(project, root) {
  if (!dir.exists(root)) {
    dir.create(root, recursive = TRUE)
  }
  file.copy(file.path(project, "orderly_config.yml"), file.path(root, "orderly_config.yml"), overwrite = TRUE)
  file.copy(file.path(project, "src"), root, recursive = TRUE, overwrite = TRUE)
  if (!dir.exists(file.path(root, ".outpack"))) {
    orderly::orderly_init(root, use_file_store = FALSE, require_complete_tree = FALSE, force = TRUE)
  }
}

ensure_remote <- function(root, remote, remote_path) {
  if (is.null(remote)) {
    return(invisible(NULL))
  }
  if (!(remote %in% orderly::orderly_location_list(root = root))) {
    if (is.null(remote_path)) {
      stop(sprintf("Orderly location '%s' is not registered in %s and no --remote-path was given", remote, root))
    }
    if (!dir.exists(file.path(remote_path, ".outpack"))) {
      orderly::orderly_init(remote_path, use_file_store = TRUE, require_complete_tree = FALSE)
    }
    orderly::orderly_location_add_path(remote, path = remote_path, root = root)
  }
  orderly::orderly_location_fetch_metadata(remote, root = root)
}

project <- dat$project
root <- dat$root
remote <- dat$remote
remote_path <- dat$remote_path
key <- jsonlite::fromJSON(dat$key_json, simplifyVector = FALSE)

ensure_root(project, root)
ensure_remote(root, remote, remote_path)

if (isTRUE(dat$fetch)) {
  clauses <- sprintf("parameter:%s == this:%s", names(key), names(key))
  expr <- sprintf("latest(%s)", paste(clauses, collapse = " && "))
  id <- orderly::orderly_search(
    expr,
    name = dat$report,
    parameters = key,
    allow_remote = !is.null(remote),
    root = root
  )
  if (length(id) == 0 || is.na(id)) {
    cat("MISS\n")
  } else {
    files <- stats::setNames(dat$artefact, basename(dat$dest))
    orderly::orderly_copy_files(
      id,
      files = files,
      dest = dirname(dat$dest),
      allow_remote = !is.null(remote),
      root = root
    )
    cat("HIT\n")
  }
} else {
  extra <- jsonlite::fromJSON(dat$extra_json, simplifyVector = FALSE)
  Sys.setenv(LEAPFROG_VALIDATE_INGEST_FILE = normalizePath(dat$source))
  id <- orderly::orderly_run(dat$report, parameters = c(key, extra), root = root, echo = FALSE)
  if (!is.null(remote)) {
    orderly::orderly_location_push(id, remote, root = root)
  }
  cat("STORED", id, "\n")
}
