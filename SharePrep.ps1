# VendorPro2026_Share.ps1 - Script to prepare for sharing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Vendor Pro 2026 - Share Preparation   " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check current folder
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: Please run this script from the Vendor-setup folder" -ForegroundColor Red
    exit 1
}

# Create share folder on Desktop
$shareFolder = "$env:USERPROFILE\Desktop\VendorPro2026_Share_$(Get-Date -Format 'yyyyMMdd')"
New-Item -Path $shareFolder -ItemType Directory -Force | Out-Null

# Copy files
$filesToCopy = @("main.py", "requirements.txt", "run.bat", "setup.bat", "README.md")
foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $shareFolder -Force
        Write-Host "  Copied: $file" -ForegroundColor Gray
    }
}

# Copy src folder
if (Test-Path "src") {
    Copy-Item -Path "src" -Destination $shareFolder -Recurse -Force
    Write-Host "  Copied: src folder" -ForegroundColor Gray
}

# Copy data folder if exists
if (Test-Path "data") {
    Copy-Item -Path "data" -Destination $shareFolder -Recurse -Force
    Write-Host "  Copied: data folder" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Share package created at:" -ForegroundColor Green
Write-Host "   $shareFolder" -ForegroundColor White
Write-Host ""
Write-Host "📦 To share with others:" -ForegroundColor Yellow
Write-Host "1. ZIP the folder above" -ForegroundColor White
Write-Host "2. Send the ZIP file to others" -ForegroundColor White
Write-Host "3. They extract and run setup.bat" -ForegroundColor White
Write-Host ""
Write-Host "🎬 Ready for distribution!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Optional: Open the folder
$open = Read-Host "Open the share folder? (Y/N)"
if ($open -eq 'Y' -or $open -eq 'y') {
    Invoke-Item $shareFolder
}
