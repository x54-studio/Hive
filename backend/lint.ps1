# Gather all .py files (recursively) and lint them one by one.
$pyscripts = Get-ChildItem -Path . -Recurse -Include *.py

foreach ($file in $pyscripts) {
    Write-Host "Linting $($file.FullName)..."
    pylint $file.FullName

    # $LASTEXITCODE is set by the last run program in PowerShell
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Pylint found errors in $($file.FullName). Aborting lint process."
        exit $LASTEXITCODE
    }
}

Write-Host "Linting complete with no errors."