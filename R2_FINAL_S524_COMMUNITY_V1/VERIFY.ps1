<#
VERIFY.ps1 -- Windows launcher for VERIFY.sh through WSL2 (Ubuntu).

This is NOT a native Windows verification. The proofs are checked INSIDE a Linux (Ubuntu) distribution that WSL2 provides; the Lean tools, the build and the
Comparator all run there. The publisher tested VERIFY.sh on native Ubuntu 24.04 only; this launcher has been parsed and dry-run on Windows, but it has not been run
against a working WSL2 Ubuntu installation by the publisher.

Usage:   .\VERIFY.ps1 -WorkDirLinux ~/r2_verify_run1 [-Distro Ubuntu] [-DryRun]
  -WorkDirLinux   a Linux path INSIDE the WSL filesystem that does not exist yet. A leading ~/ means the distribution user's home. Allowed characters: letters, digits, _ . / ~ -
                  Not under /mnt/c: builds there are slow and break file-permission handling.
  -Distro         the WSL distribution name (default Ubuntu)
  -DryRun         print the commands that would run and exit without running anything
Prerequisites inside the distribution are listed in RESTORE_AND_VERIFY.md (elan with Lean 4.34.1, Rust, Go, gcc, git, python3, >= 30 GB free disk).
#>
param(
  [Parameter(Mandatory = $true)][string]$WorkDirLinux,
  [string]$Distro = "Ubuntu",
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"
if ($WorkDirLinux -like "/mnt/*") { throw "WorkDirLinux must be inside the WSL filesystem, not under /mnt." }
if ($WorkDirLinux -notmatch '^[A-Za-z0-9_./~-]+$') { throw "WorkDirLinux may contain only letters, digits and _ . / ~ -" }
if ($Distro -notmatch '^[A-Za-z0-9_.-]+$') { throw "Distro name has unexpected characters." }
$pkgWin = $PSScriptRoot
if (-not (Test-Path (Join-Path $pkgWin "VERIFY.sh"))) { throw "VERIFY.sh not found next to this script." }
$work = $WorkDirLinux -replace '^~/', '$HOME/'       # single-quoted on purpose: the shell inside WSL expands $HOME, PowerShell does not
$stage = $work + '.pkg'
$pkgLinux = '<package path inside the distribution, from wslpath>'
$haveWsl = [bool](Get-Command wsl.exe -ErrorAction SilentlyContinue)
if ($haveWsl) {
  $p = (& wsl.exe -d $Distro -- wslpath -a $pkgWin 2>$null)
  if ($LASTEXITCODE -eq 0 -and $p -and ($p -match '^/')) { $pkgLinux = ($p | Select-Object -First 1).Trim() }
  elseif (-not $DryRun) { throw "The WSL distribution '$Distro' is not available (wsl.exe -d $Distro failed). Install it or pass -Distro." }
  else { Write-Warning "The WSL distribution '$Distro' is not available here; the dry run shows a placeholder package path." }
}
elseif (-not $DryRun) { throw "wsl.exe was not found. Install WSL2 with an Ubuntu distribution, or run VERIFY.sh on a native Ubuntu machine." }
if ($pkgLinux -match '["$`]') { throw "The package path contains characters this launcher will not pass to a shell." }
# The package is read from the Windows side; copy it into the WSL filesystem first so that file modes and line endings are Linux-correct.
$copy = 'mkdir -p "' + $stage + '" && cp -a "' + $pkgLinux + '/." "' + $stage + '/" && chmod +x "' + $stage + '/VERIFY.sh" "' + $stage + '/CONTROLS/run_controls.sh" && sed -i "s/\r$//" "' + $stage + '/VERIFY.sh" "' + $stage + '/CONTROLS/run_controls.sh"'
$run = 'cd "' + $stage + '" && ./VERIFY.sh "' + $work + '"'
Write-Host "Distribution : $Distro"
Write-Host "Package      : $pkgWin"
Write-Host "Copy step    : $copy"
Write-Host "Verify step  : $run"
if ($DryRun) { Write-Host "DRY RUN: nothing was executed."; exit 0 }
& wsl.exe -d $Distro -- bash -lc $copy
if ($LASTEXITCODE -ne 0) { throw "Copying the package into WSL failed (exit $LASTEXITCODE)." }
& wsl.exe -d $Distro -- bash -lc $run
exit $LASTEXITCODE
