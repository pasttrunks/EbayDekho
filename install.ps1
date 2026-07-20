# EbayDekho one-line installer for Windows.
# Run:  irm https://raw.githubusercontent.com/pasttrunks/EbayDekho/main/install.ps1 | iex
$ErrorActionPreference = "Stop"
$dest = Join-Path $env:USERPROFILE "EbayDekho"

Write-Host ""
Write-Host "  ===============================" -ForegroundColor Cyan
Write-Host "   EbayDekho installer" -ForegroundColor Cyan
Write-Host "  ===============================" -ForegroundColor Cyan
Write-Host ""

# 1. Python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "  Python not found - installing Python 3.12 via winget..."
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}
Write-Host "  [1/4] Python OK"

# 2. Download latest source
$zip = Join-Path $env:TEMP "ebaydekho.zip"
Invoke-WebRequest "https://codeload.github.com/pasttrunks/EbayDekho/zip/refs/heads/main" -OutFile $zip
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
Expand-Archive $zip -DestinationPath $env:TEMP -Force
Move-Item (Join-Path $env:TEMP "EbayDekho-main") $dest
Write-Host "  [2/4] Source -> $dest"

# 3. venv + deps
Push-Location $dest
python -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -q -r requirements.txt
Pop-Location
Write-Host "  [3/4] Dependencies installed"

# 4. Desktop shortcut
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut("$env:USERPROFILE\Desktop\EbayDekho.lnk")
$sc.TargetPath = "$dest\.venv\Scripts\python.exe"
$sc.Arguments = "ebaydekho.py"
$sc.WorkingDirectory = $dest
$sc.Save()
Write-Host "  [4/4] Desktop shortcut created"

Write-Host ""
Write-Host "  Done! Launching the setup wizard..." -ForegroundColor Green
Start-Process "$dest\.venv\Scripts\python.exe" -ArgumentList "ebaydekho.py" -WorkingDirectory $dest
