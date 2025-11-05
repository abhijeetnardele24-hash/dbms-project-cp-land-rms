# Clean and build PDF (requires MiKTeX/TeX Live in PATH)
$ErrorActionPreference = 'Stop'

# Move to script directory
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Clean aux files
Get-ChildItem -Include *.aux,*.bbl,*.blg,*.log,*.out,*.toc -Path . -Recurse | ForEach-Object { Remove-Item $_.FullName -Force }

# Build
pdflatex lrms_ieee.tex
bibtex lrms_ieee
pdflatex lrms_ieee.tex
pdflatex lrms_ieee.tex

Write-Host "Built paper -> lrms_ieee.pdf" -ForegroundColor Green