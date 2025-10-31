param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

function Set-EnvFromFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return }
    foreach ($line in Get-Content $Path) {
        $trimmed = $line.Trim()
        if ($trimmed.Length -eq 0 -or $trimmed.StartsWith('#')) { continue }
        $parts = $trimmed -split '=', 2
        if ($parts.Count -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            if ($name) {
                Set-Item -Path "Env:$name" -Value $value
            }
        }
    }
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $root ".venv"
$venvPython = if ($IsWindows) {
    Join-Path $venvPath "Scripts/python.exe"
} else {
    Join-Path $venvPath "bin/python"
}

if (-not (Test-Path $venvPath)) {
    Write-Host "[dev] Creating virtual environment at $venvPath"
    & $Python "-m" "venv" $venvPath
}

if (-not (Test-Path $venvPython)) {
    throw "Unable to locate python inside virtual environment at $venvPython"
}

Write-Host "[dev] Installing backend dependencies"
& $venvPython "-m" "pip" "install" "-r" (Join-Path $root "backend/requirements.txt")

Set-EnvFromFile (Join-Path $root ".env")
Set-EnvFromFile (Join-Path $root "backend/.env")

Write-Host "[dev] Applying database migrations"
Push-Location (Join-Path $root "backend")
& $venvPython "-m" "alembic" "upgrade" "head"
Pop-Location

Write-Host "[dev] Installing frontend dependencies"
Push-Location (Join-Path $root "frontend")
& npm install
Pop-Location

Write-Host "[dev] Starting backend and frontend (Ctrl+C to stop)"
$backendArgs = @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload")
$backendProcess = Start-Process -FilePath $venvPython -ArgumentList $backendArgs -WorkingDirectory (Join-Path $root "backend") -PassThru
$frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory (Join-Path $root "frontend") -PassThru

try {
    Write-Host "[dev] Backend PID: $($backendProcess.Id)"
    Write-Host "[dev] Frontend PID: $($frontendProcess.Id)"
    Wait-Process -Id @($backendProcess.Id, $frontendProcess.Id)
} finally {
    if ($backendProcess -and -not $backendProcess.HasExited) {
        Stop-Process -Id $backendProcess.Id -Force
    }
    if ($frontendProcess -and -not $frontendProcess.HasExited) {
        Stop-Process -Id $frontendProcess.Id -Force
    }
}
