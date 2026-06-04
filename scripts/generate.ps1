#Requires -Version 5.1

$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$codegenDir = Join-Path $here '..\codegen'
$uvInstallDocs = 'https://docs.astral.sh/uv/getting-started/installation/'

function Get-UvCommand {
    $command = Get-Command uv -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $candidateDirs = @(
        (Join-Path $env:USERPROFILE '.local\bin'),
        (Join-Path $env:USERPROFILE '.cargo\bin')
    )

    foreach ($dir in $candidateDirs) {
        if ((Test-Path $dir) -and ($env:PATH -notlike "*$dir*")) {
            $env:PATH = "$dir;$env:PATH"
        }
    }

    $command = Get-Command uv -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    return $null
}

$uvCommand = Get-UvCommand
if (-not $uvCommand) {
    $userResponse = Read-Host "Couldn't find uv on your system, would you like to install uv? (y/n)"
    if ($userResponse -ieq 'y') {
        try {
            Invoke-RestMethod 'https://astral.sh/uv/install.ps1' | Invoke-Expression
        }
        catch {
            Write-Host "Couldn't install via the official installer, trying pip..."
            $pipCommand = Get-Command pip -ErrorAction SilentlyContinue
            if ($pipCommand) {
                & $pipCommand.Source install uv
            }
            else {
                Write-Host "Couldn't find pip on your system, please refer to $uvInstallDocs for other installation methods."
                exit 1
            }
        }

        $uvCommand = Get-UvCommand
        if (-not $uvCommand) {
            Write-Host "uv was installed but is not available in the current session. Restart the shell or see $uvInstallDocs"
            exit 1
        }
    }
    else {
        Write-Host "This project requires uv. You can find more general installation instructions at: $uvInstallDocs"
        exit 1
    }
}

Write-Host 'Generating C++...'
Push-Location $codegenDir
try {
    & $uvCommand run src/main.py
}
finally {
    Pop-Location
}

Write-Host @"
   (o)--(o)
  /.______.\    ribbit
  \________/
 ./        \.
( .        , )
 \ \_\\//_/ /
  ~~  ~~  ~~
"@
Write-Host 'Done'

