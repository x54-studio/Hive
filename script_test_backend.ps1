# PowerShell Script to Test Hive Backend API

# Backend API Base URL
$baseUrl = "http://localhost:5000/api"

# Test Admin Credentials
$adminEmail = "test@test.com"
$adminPassword = "test"

Write-Host "Logging in as Admin..."
$response = Invoke-RestMethod -Uri "$baseUrl/login" -Method Post -ContentType "application/json" -Body (@{email=$adminEmail; password=$adminPassword} | ConvertTo-Json)
$token = $response.access_token

if ($token) {
    Write-Host "✅ Login successful. Token received."
} else {
    Write-Host "❌ Login failed."
    Exit
}

# Create a Test Article
$articleData = @{
    title = "Test Article 2"
    content = "This is a test article 2 created via PowerShell."
} | ConvertTo-Json -Depth 2

Write-Host "Creating new article..."
$articleResponse = Invoke-RestMethod -Uri "$baseUrl/articles" -Method Post -ContentType "application/json" -Headers @{Authorization="Bearer $token"} -Body $articleData

if ($articleResponse) {
    Write-Host "✅ Article created successfully."
    Write-Host "Title: $($articleResponse.title)"
} else {
    Write-Host "❌ Failed to create article."
    Exit
}

# Fetch All Articles
Write-Host "Fetching all articles..."
$articles = Invoke-RestMethod -Uri "$baseUrl/articles" -Method Get

if ($articles) {
    Write-Host "✅ Articles fetched successfully:"
    $articles | Format-Table -AutoSize
} else {
    Write-Host "❌ Failed to fetch articles."
}
