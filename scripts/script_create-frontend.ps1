# Define project name
$projectName = "frontend"

# Step 1: Ensure the frontend folder is empty
Write-Host "Checking if $projectName folder exists and is empty..." -ForegroundColor Cyan
if (Test-Path "./$projectName") {
    Remove-Item -Recurse -Force "./$projectName"
}
New-Item -ItemType Directory -Path "./$projectName" -Force | Out-Null

# Step 2: Initialize a new React app
Write-Host "Initializing React application..." -ForegroundColor Cyan
Set-Location "./$projectName"
npm init react-app . | Out-Null

# Step 3: Install @testing-library/react for unit testing
Write-Host "Installing @testing-library/react for testing..." -ForegroundColor Cyan
npm install @testing-library/react | Out-Null

# Step 4: Create folder structure for components, pages, and styles
Write-Host "Creating additional folder structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "./src/components" -Force | Out-Null
New-Item -ItemType Directory -Path "./src/pages" -Force | Out-Null
New-Item -ItemType Directory -Path "./src/styles" -Force | Out-Null

# Step 5: Install Tailwind CSS and dependencies
Write-Host "Installing Tailwind CSS and PostCSS..." -ForegroundColor Cyan
npm install -D tailwindcss@3 postcss autoprefixer | Out-Null
npx tailwindcss init | Out-Null

#exit 0

# Step 6: Ensure tailwind.config.js exists or create it
#Write-Host "Ensuring tailwind.config.js exists..." -ForegroundColor Cyan
#if (-Not (Test-Path "./tailwind.config.js")) {
#    Write-Host "Creating tailwind.config.js..." -ForegroundColor Green
#     npx tailwindcss init | Out-Null
#} else {
#    Write-Host "tailwind.config.js already exists." -ForegroundColor Yellow
#}

# Update Tailwind configuration
Write-Host "Configuring Tailwind CSS content paths..." -ForegroundColor Cyan
$tConfigPath = "./tailwind.config.js"
(Get-Content $tConfigPath) -replace "content: \[\]", 'content: ["./src/**/*.{js,jsx,ts,tsx}"]' | Set-Content $tConfigPath

# Step 7: Ensure /src/styles/index.css exists or create it
Write-Host "Ensuring /src/styles/index.css exists..." -ForegroundColor Cyan
$indexCssPath = "./src/styles/index.css"
if (-Not (Test-Path $indexCssPath)) {
    Write-Host "Creating /src/styles/index.css with Tailwind imports..." -ForegroundColor Green
    Set-Content $indexCssPath "@tailwind base;`n@tailwind components;`n@tailwind utilities;"
} else {
    Write-Host "/src/styles/index.css already exists." -ForegroundColor Yellow
}

npm install -D cross-env | Out-Null

# Step 8: Verify npm start script in package.json
Write-Host "Verifying package.json for npm start script..." -ForegroundColor Cyan
$packageJsonPath = "./package.json"
$json = Get-Content $packageJsonPath | ConvertFrom-Json
if (-not $json.scripts.start) {
    $json.scripts.start = "cross-env react-scripts start"
    $json | ConvertTo-Json -Depth 3 | Set-Content $packageJsonPath
}

# Step 9: Start the development server
Write-Host "Starting development server..." -ForegroundColor Cyan
npm start
