@description('Azure region for all resources.')
param location string

@description('Globally-unique storage account name (lowercase letters/numbers, 3-24 chars).')
param storageAccountName string

@description('Blob container name holding the private PJNZ archive.')
param containerName string

@description('Name of the user-assigned managed identity CI authenticates as.')
param managedIdentityName string

@description('GitHub org that owns the repo whose workflows are trusted.')
param githubOrg string

@description('GitHub repo whose pull_request-triggered workflows are trusted.')
param githubRepo string

param tags object = {}

// Built-in "Storage Blob Data Reader" role. Read-only, data-plane only —
// https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage
var storageBlobDataReaderRoleId = '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: managedIdentityName
  location: location
  tags: tags
}

// Trusts GitHub-issued OIDC tokens for pull_request-triggered workflow runs
// on this exact repo — nothing else can mint a token this identity accepts.
resource githubFederatedCredential 'Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2023-01-31' = {
  parent: identity
  name: 'github-${githubOrg}-${githubRepo}-pr'
  properties: {
    issuer: 'https://token.actions.githubusercontent.com'
    subject: 'repo:${githubOrg}/${githubRepo}:pull_request'
    audiences: [
      'api://AzureADTokenExchange'
    ]
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    // Without this, anyone who can list the account key (e.g. a broader
    // Contributor grant on the resource group) gets full account-level
    // read/write via key/SAS auth, bypassing the OIDC-federated identity
    // and the container-scoped Storage Blob Data Reader role entirely.
    allowSharedKeyAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: containerName
  properties: {
    publicAccess: 'None'
  }
}

// Scoped to the container, not the storage account — CI can read PJNZ
// blobs and nothing else in this subscription.
resource ciReaderRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(container.id, identity.id, storageBlobDataReaderRoleId)
  scope: container
  properties: {
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataReaderRoleId)
  }
}

output storageAccountName string = storageAccount.name
output containerName string = container.name
output managedIdentityClientId string = identity.properties.clientId
output managedIdentityPrincipalId string = identity.properties.principalId
