$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
py -3.11 scripts/finalize_submission.py
if ($LASTEXITCODE -ne 0) { throw "Lab finalization failed; review the output." }
