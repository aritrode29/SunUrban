# GitHub Pages Setup Guide

This guide will help you deploy your landing page to GitHub Pages.

## Prerequisites

1. A GitHub account (username: `aritrode29`)
2. Git installed on your computer
3. This repository initialized as a Git repository

## Setup Steps

### 1. Initialize Git Repository (if not already done)

```powershell
# Navigate to your project directory
cd "G:\My Drive\UT_Austin_MSSD\Proposals\MIC_Javad-CAEE\LandingPage_SunnyGrids"

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Landing page for GitHub Pages"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named `LandingPage_SunnyGrids` (or any name you prefer)
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

### 3. Connect Local Repository to GitHub

```powershell
# Add remote repository (replace with your actual repository name)
git remote add origin https://github.com/aritrode29/LandingPage_SunnyGrids.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select:
   - **Source**: `GitHub Actions`
5. The workflow will automatically deploy when you push to the `main` branch

### 5. Access Your Website

After the workflow runs (usually takes 1-2 minutes), your site will be available at:
```
https://aritrode29.github.io/LandingPage_SunnyGrids/
```

(Replace `LandingPage_SunnyGrids` with your actual repository name)

## How It Works

The `.github/workflows/deploy.yml` file automatically:
- Triggers on every push to `main` branch
- Deploys the `landing_page` folder to GitHub Pages
- Makes your site publicly accessible

## Updating Your Site

Simply make changes to your files and push to GitHub:

```powershell
git add .
git commit -m "Update landing page"
git push
```

The site will automatically update within 1-2 minutes.

## Troubleshooting

### Workflow Not Running
- Check that GitHub Pages is set to use "GitHub Actions" as the source
- Verify the workflow file is in `.github/workflows/deploy.yml`
- Check the "Actions" tab in your GitHub repository for any errors

### Site Not Loading
- Wait a few minutes after pushing (deployment takes time)
- Check the "Actions" tab to see if deployment succeeded
- Verify your repository name matches the URL

### File Path Issues
- All file paths in your HTML are relative, so they should work correctly
- If images don't load, check that image paths are correct relative to the HTML file

## Custom Domain (Optional)

If you want to use a custom domain:
1. Go to repository Settings → Pages
2. Enter your custom domain
3. Follow GitHub's instructions for DNS configuration

