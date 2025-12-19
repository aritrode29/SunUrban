# GitHub Repository Setup Script
# This script helps you create a GitHub repository and push your code

Write-Host "=== GitHub Repository Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if remote already exists
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote 'origin' already exists: $remoteExists" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "Exiting. Please remove the remote manually if needed." -ForegroundColor Red
        exit
    }
    git remote remove origin
}

# Get repository name
$repoName = Read-Host "Enter your GitHub repository name (e.g., LandingPage_SunnyGrids)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "LandingPage_SunnyGrids"
    Write-Host "Using default name: $repoName" -ForegroundColor Yellow
}

# GitHub username
$username = "aritrode29"
$repoUrl = "https://github.com/$username/$repoName.git"

Write-Host ""
Write-Host "Repository URL will be: $repoUrl" -ForegroundColor Green
Write-Host ""

# Instructions
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://github.com/new" -ForegroundColor Yellow
Write-Host "2. Repository name: $repoName" -ForegroundColor Yellow
Write-Host "3. Make it Public (or Private if you prefer)" -ForegroundColor Yellow
Write-Host "4. DO NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
Write-Host "5. Click 'Create repository'" -ForegroundColor Yellow
Write-Host ""
$continue = Read-Host "Have you created the repository? (y/n)"

if ($continue -ne "y") {
    Write-Host "Please create the repository first, then run this script again." -ForegroundColor Red
    exit
}

# Add remote and push
Write-Host ""
Write-Host "Adding remote and pushing code..." -ForegroundColor Cyan
git remote add origin $repoUrl
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Success! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your code has been pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/$username/$repoName/settings/pages" -ForegroundColor Yellow
    Write-Host "2. Under 'Source', select 'GitHub Actions'" -ForegroundColor Yellow
    Write-Host "3. Your site will be available at: https://$username.github.io/$repoName/" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=== Error ===" -ForegroundColor Red
    Write-Host "Failed to push. Please check:" -ForegroundColor Red
    Write-Host "1. Repository exists on GitHub" -ForegroundColor Yellow
    Write-Host "2. You have authentication set up (Git Credential Manager or SSH key)" -ForegroundColor Yellow
    Write-Host "3. You have push permissions to the repository" -ForegroundColor Yellow
    Write-Host ""
}


