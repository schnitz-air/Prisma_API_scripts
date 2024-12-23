# Import required modules
$config = @{
    PrismaCloudApiBaseUrl = $env:PRISMA_API_URL
    AccessKeyEnvVar = "PRISMA_ACCESS_KEY"
    SecretKeyEnvVar = "PRISMA_SECRET_KEY"
}
################################################################################################
# This function writes log messages to both the console and a log file
function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    #Write-Output $logMessage
    $logMessage | Out-File -Append -FilePath "PrismaCloudScript.log"
}
################################################################################################
# Function to get secrets from Azure Key Vault
# This ensures secure handling of sensitive information like credentials
function Get-SecretFromKeyVault {
    param (
        [string]$SecretName
    )
    try {
        $secret = Get-AzKeyVaultSecret -VaultName $config.KeyVaultName -Name $SecretName -AsPlainText
        return $secret
    }
    catch {
        Write-Log "Failed to retrieve secret $SecretName from Key Vault: $_" -Level "ERROR"
        throw
    }
}
################################################################################################
# Function to make API calls
# This centralizes API communication logic and error handling
function Invoke-PrismaCloudApi {
    param (
        [string]$Endpoint,
        [string]$Method,
        [hashtable]$Headers,
        [string]$Body
    )
    try {
        $uri = "$($config.PrismaCloudApiBaseUrl)$Endpoint"
        $params = @{
            Uri = $uri
            Method = $Method
            Headers = $Headers
        }
        if ($Body) {
            $params.Body = $Body
        }
        $response = Invoke-RestMethod @params -ErrorAction Stop
        return $response
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $statusDescription = $_.Exception.Response.StatusDescription
        
        $responseBody = $_.ErrorDetails.Message
        if (-not $responseBody) {
            $responseBody = $_.Exception.Message
        }
        
        Write-Log "API call to $Endpoint failed with status code $statusCode ($statusDescription)" -Level "ERROR"
        Write-Log "Response body: $responseBody" -Level "ERROR"
        Write-Log "Request body: $Body" -Level "ERROR"
        throw
    }
}
################################################################################################
# Retrieves values from environment variables, providing a consistent and secure way to access configuration.
function Get-EnvironmentVariable {
    param (
        [string]$EnvVarName
    )
    try {
        $value = [Environment]::GetEnvironmentVariable($EnvVarName)
        if ([string]::IsNullOrEmpty($value)) {
            throw "Environment variable $EnvVarName is not set or empty"
        }
        return $value
    }
    catch {
        Write-Log ("Failed to retrieve environment variable {0}: {1}" -f $EnvVarName, $_) -Level "ERROR"
        throw
    }
}
################################################################################################
# Add a function to get TargetRoleName from user
function Get-TargetRoleName {
    $roleName = Read-Host "Enter the target role name"
    while ([string]::IsNullOrWhiteSpace($roleName)) {
        Write-Log "Role name cannot be empty. Please try again." -Level "WARN"
        $roleName = Read-Host "Enter the target role name"
    }
    return $roleName
}
################################################################################################
# Update the Get-PrismaCloudRoleId function
function Get-PrismaCloudRoleId {
    param (
        [string]$Token,
        [string]$TargetRoleName
    )
    $headers = @{
        'Content-Type' = 'application/json; charset=UTF-8'
        'Accept' = 'application/json; charset=UTF-8'
        "x-redlock-auth" = $Token
    }
    $roles = Invoke-PrismaCloudApi -Endpoint "/user/role" -Method "Get" -Headers $headers
    $roleId = $roles | Where-Object {$_.name -eq $TargetRoleName} | Select-Object -ExpandProperty id
    if (-not $roleId) {
        Write-Log "Role '$TargetRoleName' not found" -Level "ERROR"
        throw "Role not found"
    }
    return $roleId
}
################################################################################################
# Authenticates with Prisma Cloud and retrieves an access token for API operations.
function Get-PrismaCloudToken {
    $accessKey = Get-EnvironmentVariable -EnvVarName $config.AccessKeyEnvVar
    $secretKey = Get-EnvironmentVariable -EnvVarName $config.SecretKeyEnvVar

    $headers = @{
        'Content-Type' = 'application/json; charset=UTF-8'
        'Accept' = 'application/json; charset=UTF-8'
    }
    $body = @{
        username = $accessKey
        password = $secretKey
    } | ConvertTo-Json

    $response = Invoke-PrismaCloudApi -Endpoint "/login" -Method "Post" -Headers $headers -Body $body
    return $response.token
}
################################################################################################
# Retrieves the ID of a specified role from Prisma Cloud.
function Get-PrismaCloudRoleId {
    param (
        [string]$Token
    )
    $headers = @{
        'Content-Type' = 'application/json; charset=UTF-8'
        'Accept' = 'application/json; charset=UTF-8'
        "x-redlock-auth" = $Token
    }
    $roles = Invoke-PrismaCloudApi -Endpoint "/user/role" -Method "Get" -Headers $headers
    $roleId = $roles | Where-Object {$_.name -eq $config.TargetRoleName} | Select-Object -ExpandProperty id
    if (-not $roleId) {
        Write-Log "Role '$($config.TargetRoleName)' not found" -Level "ERROR"
        throw "Role not found"
    }
    return $roleId
}
################################################################################################
# Fetches the list of repositories currently integrated with Prisma Cloud.
function Get-PrismaCloudRepositories {
    param ([string]$Token)
    $headers = @{
        "Cache-Control" = "no-cache"
        "Accept" = "application/json"
        "Accept-Encoding" = "gzip, deflate, br"
        "Connection" = "keep-alive"
        "authorization" = $Token
    }
    $repositories = Invoke-PrismaCloudApi -Endpoint "/code/api/v2/repositories" -Method "Get" -Headers $headers
    if ($null -eq $repositories) {
        Write-Log "API returned null for repositories" -Level "WARN"
        return @()
    }
    return $repositories
}
################################################################################################
# Adds new repositories to Prisma Cloud for monitoring.
function Add-PrismaCloudRepositories {
    param (
        [string]$Token,
        [string[]]$Repositories,
        [string]$IntegrationId
    )
    $headers = @{
        'Content-Type' = 'application/json'
        'Accept' = 'application/json'
        "authorization" = $Token
    }
    $bodyContent = @{
        integrationId = $IntegrationId
        repositoriesNames = $Repositories
        skipNonExistsRepositories = $true
    }
    $body = $bodyContent | ConvertTo-Json -Depth 3

    Write-Log "Request body: $body"
    $response = Invoke-PrismaCloudApi -Endpoint "/code/api/v2/repositories" -Method "Post" -Headers $headers -Body $body
    #Write-Host ($bodyContent | ConvertTo-Json -Depth 3)
    #Write-Host $response
    return $response
}
################################################################################################
# Reads repository names from a file, allowing for bulk import of repository lists.
function Get-RepositoriesFromFile {
    param (
        [string]$FilePath
    )
    if (-not (Test-Path $FilePath)) {
        Write-Log "Repository list file not found: $FilePath" -Level "ERROR"
        throw "File not found"
    }
    $repositories = @(Get-Content $FilePath | Where-Object { 
        $_ -match '\S' -and 
        $_ -notmatch '^\s*#' -and 
        ($_ -match '^[\w-]+/[\w-]+' -or $_ -match '^[\w-]+/[\w-]+/[\w-]+')
    } | ForEach-Object { $_.Trim() })
    #write-host "*************" @repositories
    Write-Log "Read $($repositories.Count) repositories from file"
    return $repositories
}
################################################################################################
# Retrieves Azure Repos integrations from Prisma Cloud.
function Get-AzureReposIntegrations {
    param (
        [string]$Token
    )
    $headers = @{
        'Content-Type' = 'application/json'
        'Accept' = 'application/json'
        "authorization" = $Token
    }
    $response = Invoke-PrismaCloudApi -Endpoint "/code/api/v2/integrations" -Method "Get" -Headers $headers
    
    $jsonResponse = $response | ConvertFrom-Json -AsHashtable
    
    $azureReposIntegrations = $jsonResponse.data | 
        Where-Object { $_.type -eq "AzureRepos" } | 
        ForEach-Object {
            [PSCustomObject]@{
                Id = $_.id
                EmailAddress = $_.params.profile.emailAddress
                DisplayName = $_.params.profile.displayName
            }
        }
    
    Write-Log "Found $($azureReposIntegrations.Count) Azure Repos integrations"
    $azureReposIntegrations | ForEach-Object {
        Write-Log "Integration ID: $($_.Id), Email: $($_.EmailAddress), Display Name: $($_.DisplayName), Repositories: $($_.Repositories), Status: $($_.Status), Last Updated: $($_.LastUpdated)"
    } 
    return $azureReposIntegrations
}    
################################################################################################
# Main function that allows users to choose repository type and execute appropriate onboarding function.
function Start-RepositoryOnboarding {
    $repoTypes = @("AzureRepos", "Github", "Gitlab", "Bitbucket")
    
    # Get the TargetRoleName from the user
    $script:TargetRoleName = Get-TargetRoleName
    
    while ($true) {
        $selectedType = Show-Menu -Title "Select Repository Type" -Options $repoTypes

        switch ($selectedType) {
            "AzureRepos" { 
                Start-AzureReposOnboarding 
                return
            }
            "Github" { 
                Start-GitHubOnboarding 
                return
            }
            "Gitlab" { 
                Write-Host "Under Development - Coming up soon"
                continue
            }
            "Bitbucket" { 
                Write-Host "Under Development - Coming up soon"
                continue
            }
            default { 
                Write-Log "Invalid repository type selected." -Level "ERROR"
                continue
            }
        }
    }
}
# Handles the onboarding process for Azure Repos.
function Start-AzureReposOnboarding {
    Write-Log "Starting Azure Repos onboarding process"
    $repoListFile = Get-RepositoryListFile
    $repositories = Get-RepositoriesFromFile -FilePath $repoListFile
    Write-Host "`n === Identified the following repositories from file ==="
    foreach ($repo in $repositories) {
        Write-Host $repo
    }
    
    $confirmation = Read-Host "Do you want to proceed with onboarding these repositories? (Y/N)"
    if ($confirmation -ne 'Y') {
        Write-Log "User cancelled Azure Repos onboarding"
        return
    }
    
    if (Test-AzureReposFormat -Repositories $repositories) {
        $token = Get-PrismaCloudToken
        $integrationId = Get-AzureReposIntegrationId -Token $token
        Add-AzureReposRepositories -Token $token -Repositories $repositories -IntegrationId $integrationId
    }
}
################################################################################################
# Helper function to show a menu and get user selection
function Show-Menu {
    param (
        [string]$Title,
        [string[]]$Options
    )
    Write-Host "=== $Title ==="
    for ($i=0; $i -lt $Options.Count; $i++) {
        Write-Host "$($i+1). $($Options[$i])"
    }
    do {
        $selection = Read-Host "Enter your choice (1-$($Options.Count))"
    } while ($selection -lt 1 -or $selection -gt $Options.Count)
    return $Options[$selection-1]
}
################################################################################################
# Function to get repository list file
function Get-RepositoryListFile {
    $defaultFile = Join-Path $PSScriptRoot "repolist.txt"
    if (Test-Path $defaultFile) {
        return $defaultFile
    } else {
        return Read-Host "Enter the path to the repository list file"
    }
}
################################################################################################
# Validates if repositories are in the correct Azure Repos format.
function Test-AzureReposFormat {
    param ([string[]]$Repositories)
    $pattern = '^[\w-]+(/[\w-]+)+$'
    $invalidRepos = $Repositories | Where-Object { $_ -notmatch $pattern }
    if ($invalidRepos) {
        Write-Log "The following repositories are not in the correct 'Organization/Project/Repository' format:" -Level "ERROR"
        $invalidRepos | ForEach-Object { Write-Log $_ -Level "ERROR" }
        return $false
    }
    return $true
}
################################################################################################
# Retrieves the integration ID for Azure Repos.
function Get-AzureReposIntegrationId {
    param ([string]$Token)
    
    $integrations = Get-AzureReposIntegrations -Token $Token
    if ($integrations.Count -eq 0) {
        throw "No Azure Repos integrations found."
    } elseif ($integrations.Count -eq 1) {
        $selectedId = $integrations[0].Id
        Write-Log "Single integration found. Using ID: $selectedId"
    } else {
            $selectedOption = Show-Menu -Title "Select Azure Repos Integration" -Options ($integrations | ForEach-Object { "$($_.DisplayName) ($($_.EmailAddress)) ($($_.Id))" })
            $selectedId = if ($selectedOption -match '\(([\w-]{36})\)') {
                $matches[1]
            } else {
                throw "Unable to extract integration ID from selection"
            }
            Write-Log "Multiple integrations found. Selected integration ID: $selectedId"
    }
    Write-Log "Returning integration ID: $selectedId"
    return $selectedId
}
################################################################################################
#Adds Azure Repos repositories to Prisma Cloud.
function Add-AzureReposRepositories {
    param (
        [string]$Token,
        [string[]]$Repositories,
        [string]$IntegrationId
    )
    Write-Log "Add-AzureReposRepositories received IntegrationId: $IntegrationId"
    $headers = @{
        'Content-Type' = 'application/json'
        'Accept' = 'application/json'
        "authorization" = $Token
    }

    $formattedRepos = $Repositories | ForEach-Object {
        if ($_ -match '^([\w-]+)/([\w-]+)/([\w-]+)') {
            "$($Matches[1])/$($Matches[2])/$($Matches[3])"
        } else {
            Write-Log "Invalid repository format: $_. Skipping." -Level "WARN"
            $null
        }
    } | Where-Object { $_ -ne $null }

    $bodyContent = @{
        integrationId = $IntegrationId
        repositoriesNames = @($formattedRepos)
        skipNonExistsRepositories = $true
    }
    $body = $bodyContent | ConvertTo-Json -Depth 3

    #Write-host "Request body: $body"

    $response = Invoke-PrismaCloudApi -Endpoint "/code/api/v2/repositories" -Method "Post" -Headers $headers -Body $body
    Write-Host ($bodyContent | ConvertTo-Json -Depth 3)
    return $response
}
################################################################################################# Main script execution
# Handles the onboarding process for GitHub repositories.
function Start-GitHubOnboarding {
    Write-Log "Starting GitHub onboarding process"
    $repoListFile = Get-RepositoryListFile
    $repositories = Get-RepositoriesFromFile -FilePath $repoListFile
    Write-Host "`n === Identified the following repositories from file ==="
    foreach ($repo in $repositories) {
        Write-Host $repo
    }
    
    $confirmation = Read-Host "Do you want to proceed with onboarding these repositories? (Y/N)"
    if ($confirmation -ne 'Y') {
        Write-Log "User cancelled GitHub onboarding"
        return
    }
    
    if (Test-GitHubReposFormat -Repositories $repositories) {
        $token = Get-PrismaCloudToken
        $integrationId = Get-GitHubIntegrationId -Token $token
        Add-GitHubRepositories -Token $token -Repositories $repositories -IntegrationId $integrationId
    }
}
#################################################################################################
# Validates if repositories listed in the file are in the correct format for GitHub onboarding.
function Test-GitHubReposFormat {
    param ([string[]]$Repositories)
    $pattern = '^[\w-]+/[\w-]+$'
    $invalidRepos = $Repositories | Where-Object { $_ -notmatch $pattern }
    if ($invalidRepos) {
        Write-Log "The following repositories are not in the correct 'Owner/Repository' format:" -Level "ERROR"
        $invalidRepos | ForEach-Object { Write-Log $_ -Level "ERROR" }
        return $false
    }
    return $true
}
#################################################################################################
# Retrieves GitHub integrations from Prisma Cloud.
function Get-GitHubIntegrations {
    param ([string]$Token)
    $headers = @{
        'Content-Type' = 'application/json'
        'Accept' = 'application/json'
        "authorization" = $Token
    }
    $response = Invoke-PrismaCloudApi -Endpoint "/code/api/v2/integrations" -Method "Get" -Headers $headers
    
    $jsonResponse = $response | ConvertFrom-Json -AsHashtable
    
    $githubIntegrations = $jsonResponse.data | 
        Where-Object { $_.type -eq "GitHub" } | 
        ForEach-Object {
            [PSCustomObject]@{
                Id = $_.id
                Name = $_.name
                DisplayName = $_.params.profile.displayName
            }
        }
    
    Write-Log "Found $($githubIntegrations.Count) GitHub integrations"
    return $githubIntegrations
}
#################################################################################################
# Retrieves the GitHub integration ID from Prisma Cloud. If multiple integrations are found, it prompts the user to select one.
function Get-GitHubIntegrationId {
    param ([string]$Token)
    
    $integrations = Get-GitHubIntegrations -Token $Token
    if ($integrations.Count -eq 0) {
        throw "No GitHub integrations found."
    } elseif ($integrations.Count -eq 1) {
        $selectedId = $integrations[0].Id
        Write-Log "Single integration found. Using ID: $selectedId"
    } else {
        $selectedOption = Show-Menu -Title "Select GitHub Integration" -Options ($integrations | ForEach-Object { "$($_.Name) ($($_.DisplayName)) ($($_.Id))" })
        $selectedId = if ($selectedOption -match '\(([\w-]{36})\)') {
            $matches[1]
        } else {
            throw "Unable to extract integration ID from selection"
        }
        Write-Log "Multiple integrations found. Selected integration ID: $selectedId"
    }
    Write-Log "Returning integration ID: $selectedId"
    return $selectedId
}
#################################################################################################
# Adds GitHub repositories to Prisma Cloud for monitoring. This function takes a Prisma Cloud API token, an array of repository names, and an integration ID, then sends a request to add these repositories to the specified integration.
function Add-GitHubRepositories {
    param (
        [string]$Token,
        [string[]]$Repositories,
        [string]$IntegrationId
    )
    Write-Log "Add-GitHubRepositories received IntegrationId: $IntegrationId"
    $headers = @{
        'Content-Type' = 'application/json'
        'Accept' = 'application/json'
        "authorization" = $Token
    }

    $bodyContent = @{
        integrationId = $IntegrationId
        repositoriesNames = @($Repositories)
        skipNonExistsRepositories = $true
    }
    $body = $bodyContent | ConvertTo-Json -Depth 3

    #Write-Host "Request body: $body"

    $response = Invoke-PrismaCloudApi -Endpoint "/code/api/v2/repositories" -Method "Post" -Headers $headers -Body $body
    #Write-Host ($bodyContent | ConvertTo-Json -Depth 3)
    return $response
}
#################################################################################################
# Main script execution
Start-RepositoryOnboarding
