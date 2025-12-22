# Fix GitHub Pages - Showing README Instead of Website

## Problem
GitHub Pages is showing the README.md file instead of your website. This means GitHub Pages is configured to deploy from a branch instead of using GitHub Actions.

## Solution - Enable GitHub Actions Deployment

### Step 1: Go to Repository Settings
1. Go to: **https://github.com/aritrode29/SunUrban/settings/pages**

### Step 2: Change Source to GitHub Actions
1. Under **"Source"** section, you'll see options like:
   - ❌ **Deploy from a branch** (This is probably selected - WRONG!)
   - ✅ **GitHub Actions** (This is what we need!)

2. **Select "GitHub Actions"** as the source
3. Click **"Save"**

### Step 3: Verify Workflow Runs
1. Go to: **https://github.com/aritrode29/SunUrban/actions**
2. You should see **"Deploy to GitHub Pages"** workflow
3. It should run automatically and show a green checkmark when complete

### Step 4: Wait and Check
- Wait 1-2 minutes for deployment
- Visit: **https://aritrode29.github.io/SunUrban/**
- You should now see your website (index.html) instead of README

## If GitHub Actions Option Doesn't Appear

If you don't see "GitHub Actions" as an option:

1. **Check Workflow File Exists**:
   - Go to: `.github/workflows/deploy.yml`
   - Make sure it exists and is committed

2. **Check Repository Permissions**:
   - Go to: Settings → Actions → General
   - Under "Workflow permissions", select:
     - ✅ "Read and write permissions"
     - ✅ "Allow GitHub Actions to create and approve pull requests"

3. **Manually Trigger Workflow**:
   - Go to: Actions tab
   - Click "Deploy to GitHub Pages"
   - Click "Run workflow" button
   - Select "main" branch
   - Click "Run workflow"

## Quick Checklist

- [ ] GitHub Pages Source is set to **"GitHub Actions"** (NOT "Deploy from a branch")
- [ ] Workflow file exists: `.github/workflows/deploy.yml`
- [ ] Workflow has run successfully (check Actions tab)
- [ ] Wait 2-3 minutes after enabling
- [ ] Clear browser cache (Ctrl+Shift+R)
- [ ] Visit: https://aritrode29.github.io/SunUrban/

## Still Not Working?

If it's still showing README after following these steps:

1. **Check Actions Logs**:
   - Go to Actions tab
   - Click on the latest "Deploy to GitHub Pages" run
   - Check for any red X marks or errors
   - Look at the "Deploy to GitHub Pages" step for errors

2. **Verify File Structure**:
   - Make sure `landing_page/index.html` exists
   - Make sure `.nojekyll` file exists in `landing_page/` directory

3. **Try Manual Trigger**:
   - Actions → Deploy to GitHub Pages → Run workflow

---

**The key fix**: Change GitHub Pages source from "Deploy from a branch" to **"GitHub Actions"** in repository settings!
