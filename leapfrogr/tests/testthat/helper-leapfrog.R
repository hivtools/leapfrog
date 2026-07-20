skip_for_compilation <- function() {
  testthat::skip_on_cran()
}

skip_if_no_test_data <- function() {
  required_files <- c(
    "adult_parms_full.h5",
    "adult_parms_coarse.h5",
    "child_test_utils.rds",
    "child_parms_full.h5",
    "child_parms_coarse.h5",
    "spectrum_params.h5"
  )
  required_file_paths <- unlist(lapply(required_files, function(f) {
    testthat::test_path(sprintf("testdata/%s", f))
  }))

  if (!all(file.exists(required_file_paths))) {
    testthat::skip("
Ribbit?
       _   _
      (.)_(.)
   _ (   _   ) _
  / \\/`-----'\\/ \\
__\\ ( (     ) ) /__
)   /\\ \\._./ /\\   (
 )_/ /|\\   /|\\ \\_(

Oops, looks like you don't have the test data generated, please run scripts/create_test_data.R from the root of the package!
")
  }
}

copy_directory <- function(src, as) {
  files <- dir(src, all.files = TRUE, no.. = TRUE, full.names = TRUE)
  dir.create(as, FALSE, TRUE)
  ok <- file.copy(files, as, recursive = TRUE)
  if (!all(ok)) {
    stop("Error copying files")
  }
}

expect_contains <- function(expected, full_text) {
  expect_true(any(grepl(expected, full_text, fixed = TRUE)))
}

expect_string <- function(x, err_msg = deparse(substitute(x))) {
  expect_true(!is.na(x) && nzchar(x),
              sprintf("Expected non empty string: %s", err_msg))
}

expect_named <- function(x, err_msg = deparse(substitute(x))) {
  expect_true(!is.null(names(x)),
              sprintf("%s is not named", err_msg))
  expect_true(!any(duplicated(names(x))),
              sprintf("%s has duplicate names", err_msg))
}
