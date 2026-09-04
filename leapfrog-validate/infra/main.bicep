targetScope = 'subscription'

@description('Azure region for all resources. eastus by default — GitHub-hosted standard runners have historically run out of US Azure regions (East US/East US 2/West US 2/Central US/South Central US), never officially guaranteed but the best public signal available; override if that changes or your org needs otherwise.')
param location string = 'eastus'

@description('Name of the resource group to create.')
param resourceGroupName string = 'pjnz-archive-rg'

@description('Globally-unique storage account name (lowercase letters/numbers, 3-24 chars). Change if taken.')
@minLength(3)
@maxLength(24)
param storageAccountName string = 'pjnzarchive'

@description('Blob container name holding the private PJNZ archive.')
param containerName string = 'pjnz-archive'

@description('Name of the user-assigned managed identity CI authenticates as. Repo-specific by nature (its federated credential is bound to one GitHub repo), unlike the storage account/container which are named generically since other consumers may read the same archive later.')
param managedIdentityName string = 'leapfrog-ci-reader'

@description('GitHub org that owns the repo whose workflows are trusted.')
param githubOrg string = 'hivtools'

@description('GitHub repo whose pull_request-triggered workflows are trusted.')
param githubRepo string = 'leapfrog'

var tags = {
  project: 'pjnz-archive'
}

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module archive 'modules/archive.bicep' = {
  name: 'archive-resources'
  scope: rg
  params: {
    location: location
    storageAccountName: storageAccountName
    containerName: containerName
    managedIdentityName: managedIdentityName
    githubOrg: githubOrg
    githubRepo: githubRepo
    tags: tags
  }
}

output resourceGroupName string = rg.name
output storageAccountName string = archive.outputs.storageAccountName
output containerName string = archive.outputs.containerName
output managedIdentityClientId string = archive.outputs.managedIdentityClientId
// Echoed back so deploy.sh publishes GitHub variables on the repo this
// deployment actually trusted, not a second, independently-typed guess.
output githubOrg string = githubOrg
output githubRepo string = githubRepo
output tenantId string = subscription().tenantId
output subscriptionId string = subscription().subscriptionId
