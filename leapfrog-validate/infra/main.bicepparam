using 'main.bicep'

// Mirrors main.bicep's own parameter defaults -- this file is the actual
// deployment's source of truth; main.bicep's defaults exist so `az
// deployment sub create --template-file main.bicep` also works standalone
// (e.g. ad-hoc testing) without one. Keep both in sync if either changes.
param location = 'eastus'
param resourceGroupName = 'pjnz-archive-rg'
param storageAccountName = 'pjnzarchive'
param containerName = 'pjnz-archive'
param managedIdentityName = 'leapfrog-ci-reader'
param githubOrg = 'hivtools'
param githubRepo = 'leapfrog'
