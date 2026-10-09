#!/usr/bin/env bash
#
# Deploys the PJNZ archive Azure infra (main.bicep) and publishes the
# resulting CI identity details as GitHub repo variables on whichever repo
# main.bicepparam's githubOrg/githubRepo point at (hivtools/leapfrog by
# default). GitHub variables aren't an Azure resource, so this step lives
# outside Bicep as a thin bridge.
#
# Prerequisites:
#   - az CLI logged in (az login) to the target subscription, with Owner or
#     Contributor + User Access Administrator on it (creating the RBAC role
#     assignment needs the latter).
#   - gh CLI authenticated against whichever repo main.bicepparam targets.
#   - jq installed.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

LOCATION="${LOCATION:-eastus}"
DEPLOYMENT_NAME="pjnz-archive-$(date +%Y%m%d%H%M%S)"

echo "Subscription context:"
az account show --query '{name:name, id:id, tenantId:tenantId}' -o table

echo
echo "Previewing changes (what-if)..."
az deployment sub what-if \
  --location "$LOCATION" \
  --template-file main.bicep \
  --parameters main.bicepparam

echo
read -rp "Proceed with deployment? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

az deployment sub create \
  --name "$DEPLOYMENT_NAME" \
  --location "$LOCATION" \
  --template-file main.bicep \
  --parameters main.bicepparam

outputs=$(az deployment sub show --name "$DEPLOYMENT_NAME" --query properties.outputs -o json)

client_id=$(jq -r '.managedIdentityClientId.value' <<<"$outputs")
tenant_id=$(jq -r '.tenantId.value' <<<"$outputs")
subscription_id=$(jq -r '.subscriptionId.value' <<<"$outputs")
storage_account=$(jq -r '.storageAccountName.value' <<<"$outputs")
container=$(jq -r '.containerName.value' <<<"$outputs")
github_repo=$(jq -r '.githubOrg.value + "/" + .githubRepo.value' <<<"$outputs")

echo
echo "Publishing GitHub repo variables on $github_repo..."
gh variable set AZURE_CLIENT_ID --repo "$github_repo" --body "$client_id"
gh variable set AZURE_TENANT_ID --repo "$github_repo" --body "$tenant_id"
gh variable set AZURE_SUBSCRIPTION_ID --repo "$github_repo" --body "$subscription_id"
gh variable set AZURE_STORAGE_ACCOUNT --repo "$github_repo" --body "$storage_account"
gh variable set AZURE_STORAGE_CONTAINER --repo "$github_repo" --body "$container"

echo
echo "Done. A workflow can now authenticate via OIDC using these variables"
echo "(azure/login@v2 with client-id/tenant-id/subscription-id, plus"
echo "permissions: id-token: write on the job)."
