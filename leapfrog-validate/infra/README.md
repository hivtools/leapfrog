# PJNZ archive Azure infra

Provisions the Azure storage backing the private PJNZ archive for
a private blob container plus a CI identity that authenticates via GitHub
OIDC, no static secret stored anywhere.

## What this creates

- A resource group (`pjnz-archive-rg` by default).
- A Hot-tier, LRS storage account with public blob access disabled.
- A private container (`pjnz-archive`) inside it.
- A user-assigned managed identity (`leapfrog-ci-reader`) with a federated
  credential trusting GitHub-issued OIDC tokens for `pull_request`-triggered
  workflow runs on `hivtools/leapfrog` — and nothing else.
- A `Storage Blob Data Reader` role assignment for that identity, scoped to
  the container only (not the storage account, not the subscription).

Layout: `main.bicep` is a subscription-scope template that creates the
resource group and calls `modules/archive.bicep` (resource-group scope) for
everything inside it — Bicep can't mix scopes in one file, and resource
group creation genuinely is a different scope from the resources living in
it.

## Prerequisites

- `az` CLI, logged in (`az login`) to the right subscription
  (`az account show` to check; `az account set --subscription <id>` to
  switch).
- Sufficient rights on that subscription to create a resource group, a
  storage account, and an RBAC role assignment — Owner, or
  Contributor + User Access Administrator. Role assignment creation is the
  one that needs the extra role beyond plain Contributor.
- `jq` (used by `deploy.sh` to parse deployment outputs).
- `gh` CLI authenticated against `hivtools/leapfrog` (used by `deploy.sh` to
  publish the resulting IDs as repo variables — this step is outside Bicep
  since GitHub variables aren't an Azure resource).

None of this runs from the sandbox this was authored in — it needs your own
machine, your own `az login` session.

## Deploy

```bash
cd leapfrog-validate/infra
./deploy.sh
```

This previews the change (`az deployment sub what-if`), asks for
confirmation, deploys, then writes `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`,
`AZURE_SUBSCRIPTION_ID`, `AZURE_STORAGE_ACCOUNT`, and
`AZURE_STORAGE_CONTAINER` as GitHub repo variables on `hivtools/leapfrog`.

Or drive it by hand with `az deployment sub create --location <region>
--template-file main.bicep --parameters main.bicepparam` if you'd rather
not run the wrapper.

## Uploading files

To upload files you will need the "Storage Blob Data Owner" role. You can add this via the user interface: go to Storage account -> Access Control -> Add -> Add role assignment, then add Storage Blob Data Owner to your login account. Or via CLI

```
az role assignment create --role "Storage Blob Data Owner" --assignee <your-email> --scope $(az storage account show --name pjnzarchive --resource-group pjnz-archive-rg --query id -o tsv)
```

Preferred — [azcopy](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10)
(separate install, but resumable and much faster for bulk uploads than
`az`). The trailing `/*` on the source uploads the directory's *contents*
(files plus the `ETH` subfolder) without adding an extra nested folder
named after the local directory:

```bash
azcopy login
azcopy copy \
  "/path/to/your/local/folder/*" \
  "https://pjnzarchive.blob.core.windows.net/pjnz-archive/2026%20Estimates/Public%20Spectrum%20files" \
  --recursive
```

No extra install — `az storage blob upload-batch` reuses your existing
`az login` session:

```bash
az storage blob upload-batch \
  --account-name pjnzarchive \
  --destination pjnz-archive \
  --destination-path "2026 Estimates/Public Spectrum files" \
  --source "/path/to/your/local/folder" \
  --auth-mode login
```

Either way, subfolders under the source (`ETH/`) land at the matching path
under the destination (`.../Public Spectrum files/ETH/...`) automatically.

The classifier that tags files by shape/domain properties is the rest of
ticket 16 — not covered here. A CI workflow consuming the variables above
(`azure/login@v2` with `client-id`/`tenant-id`/`subscription-id` plus
`permissions: id-token: write` on the job) is tickets 20-22's job, once the
archive and tagging exist.

If another repo/tool ever needs to read this same archive, add another
`userAssignedIdentity` + `federatedIdentityCredential` + role assignment
block to `modules/archive.bicep` scoped to that repo — the storage account
and container don't need to change.

## Fork PRs

GitHub's OIDC `sub` claim for `pull_request`-triggered runs is
`repo:hivtools/leapfrog:pull_request` for fork PRs too — the federated
credential's trust condition alone does **not** exclude forks. Today's
fork-safety comes from a separate GitHub platform default: workflows
triggered by `pull_request` from a fork don't get OIDC tokens (or secrets)
at all, regardless of what this Bicep trusts. That default is not pinned
anywhere in this infra — a future workflow using `pull_request_target`
instead of `pull_request` (tickets 20-22's territory) would defeat it with
nothing here to catch it. Gate the actual CI workflow to same-repo
branches explicitly rather than relying on this being noticed later.
