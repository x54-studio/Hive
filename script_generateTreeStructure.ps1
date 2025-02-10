# Specify the path, folders to exclude, files to exclude, and output file
$Path         = "D:\Projects\Hive"
$Exclude      = @("node_modules", ".git", "venv", "__pycache__") # List of folders to exclude
# $ExcludeFiles = @("*.ico", "*.ps1", "package-lock.json", ".gitignore", "TreeStructure.txt") # List of files to exclude
$ExcludeFiles = @("*.test1")
$OutputFile   = "TreeStructure.txt"

# Recursive function to build the tree structure
function Get-Tree {
    param (
        [string]$BasePath,
        [string]$Indent = ""
    )
    # Get all child items in the base path
    Get-ChildItem -Path $BasePath -Force | ForEach-Object {
        # Skip excluded folders and their contents
        if ($_.PSIsContainer -and $Exclude -contains $_.Name) {
            return
        }
        
        # If the item is a file, check against the excluded files list
        if (-not $_.PSIsContainer) {
            foreach ($pattern in $ExcludeFiles) {
                if ($_.Name -like $pattern) {
                    return
                }
            }
        }
        
        # Log the item into the output file
        if ($_.PSIsContainer) {
            Add-Content -Path $OutputFile -Value "$Indent[DIR] $($_.Name)"
            # Recurse into subfolders
            Get-Tree -BasePath $_.FullName -Indent "$Indent    "
        }
        else {
            Add-Content -Path $OutputFile -Value "$Indent[FILE] $($_.Name)"
        }
    }
}

# Ensure the output file is empty before starting
New-Item -Path $OutputFile -Force -ItemType File | Out-Null

# Call the function to generate the tree and save it to the file
Get-Tree -BasePath $Path

# Notify the user
Write-Host "Tree structure exported to $OutputFile"
