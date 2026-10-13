## Archive one leapfrog `run` output (ticket 24).
##
## This report does not compute anything. `leapfrog-validate` has already
## built leapfrogr at the ref and run the model; this report only records the
## raw output.h5 as a packet. The caller hands the file over through the
## LEAPFROG_VALIDATE_INGEST_FILE environment variable.
##
## Parameters:
##   pjnz           PJNZ label (file name, or corpus-relative path)
##   pjnz_sha256    SHA-256 of the PJNZ file contents
##   ref_sha        full commit SHA the model was built at
##   ref_given      the ref as the caller gave it (branch, tag, or SHA);
##                  stored for `latest(parameter:ref_given == ...)` lookups,
##                  but not part of the exact lookup key
##   configuration  leapfrog model configuration that was run
## The exact lookup key is pjnz + pjnz_sha256 + ref_sha + configuration.

params <- orderly::orderly_parameters(
  pjnz = NULL,
  pjnz_sha256 = NULL,
  ref_sha = NULL,
  ref_given = NULL,
  configuration = NULL
)
orderly::orderly_artefact(description = "Raw leapfrog model output", files = "output.h5")

ingest <- Sys.getenv("LEAPFROG_VALIDATE_INGEST_FILE")
if (!nzchar(ingest) || !file.exists(ingest)) {
  stop("LEAPFROG_VALIDATE_INGEST_FILE must name an existing output.h5")
}
file.copy(ingest, "output.h5")
