## Archive one PJNZ's extracted Spectrum modvars (ticket 24).
##
## Independent of any git ref: reading a PJNZ's Spectrum modvars does not
## depend on leapfrog's source. The caller hands the already-extracted
## extract.h5 over through the LEAPFROG_VALIDATE_INGEST_FILE environment
## variable. The packet holds raw modvars, not indicators: indicator
## extraction stays a live function.
##
## Parameters:
##   pjnz         PJNZ label (file name, or corpus-relative path)
##   pjnz_sha256  SHA-256 of the PJNZ file contents
##   importer     version of the PJNZ importer that read the modvars
##                (provenance only, not part of the exact lookup key)
## The exact lookup key is pjnz + pjnz_sha256.

params <- orderly::orderly_parameters(
  pjnz = NULL,
  pjnz_sha256 = NULL,
  importer = NULL
)
orderly::orderly_artefact(description = "Extracted Spectrum modvars", files = "extract.h5")

ingest <- Sys.getenv("LEAPFROG_VALIDATE_INGEST_FILE")
if (!nzchar(ingest) || !file.exists(ingest)) {
  stop("LEAPFROG_VALIDATE_INGEST_FILE must name an existing extract.h5")
}
file.copy(ingest, "extract.h5")
