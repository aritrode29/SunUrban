# Troubleshooting GitHub Pages 404 Error

## Issue: 404 File Not Found

If you're seeing a 404 error, follow these steps:

## Step 1: Enable GitHub Pages

**This is the most common cause of 404 errors!**

1. Go to: https://github.com/aritrode29/SunUrban/settings/pages
2. Under **"Source"**, select: **"GitHub Actions"** (NOT "Deploy from a branch")
3. Click **"Save"**
4. Wait 1-2 minutes for the deployment to start

## Step 2: Check Workflow Status

1. Go to: https://github.com/aritrode29/SunUrban/actions
2. Look for **"Deploy to GitHub Pages"** workflow
3. Check if it's:
   - ✅ **Green (completed)** - Deployment successful
   - ⏳ **Yellow (in progress)** - Wait for it to finish
   - ❌ **Red (failed)** - See error details below

## Step 3: Verify Files Are Deployed

After the workflow completes:

1. Go to: https://github.com/aritrode29/SunUrban/settings/pages
2. You should see: **"Your site is live at https://aritrode29.github.io/SunUrban/"**
3. If not, the deployment may have failed

## Step 4: Manual Deployment Trigger

If the workflow hasn't run automatically:

1. Go to: https://github.com/aritrode29/SunUrban/actions
2. Click **"Deploy to GitHub Pages"** in the left sidebar
3. Click **"Run workflow"** button (top right)
4. Select **"main"** branch
5. Click **"Run workflow"**
6. Wait 1-2 minutes

## Step 5: Clear Browser Cache

Sometimes browsers cache the 404 page:

- **Chrome/Edge**: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- **Firefox**: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- Or use **Incognito/Private mode**

## Step 6: Check URL

Make sure you're visiting the correct URL:

✅ **Correct**: `https://aritrode29.github.io/SunUrban/`  
❌ **Wrong**: `https://aritrode29.github.io/SunUrban/index.html` (should work but try root first)  
❌ **Wrong**: `https://github.com/aritrode29/SunUrban` (this is the repo, not the site)

## Common Issues & Solutions

### Issue: "Workflow not found"
**Solution**: Make sure `.github/workflows/deploy.yml` exists and is committed

### Issue: "Permission denied"
**Solution**: 
1. Go to Settings → Actions → General
2. Under "Workflow permissions", select "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"

### Issue: "No such file or directory"
**Solution**: Verify `landing_page/index.html` exists in the repository

### Issue: "Environment not found"
**Solution**: 
1. Go to Settings → Environments
2. Create environment named `github-pages` if it doesn't exist
3. Or remove the environment requirement from the workflow

## Verify Repository Structure

Your repository should have:
```
SunUrban/
├── .github/
│   └── workflows/
│       └── deploy.yml          ← Deployment workflow
├── landing_page/
│   ├── index.html              ← Main page (REQUIRED)
│   ├── .nojekyll               ← Prevents Jekyll processing
│   ├── styles.css
│   ├── script.js
│   └── [other HTML files]
└── README.md
```

## Quick Fix Checklist

- [ ] GitHub Pages is enabled (Settings → Pages → Source: GitHub Actions)
- [ ] Workflow has run successfully (Actions tab shows green checkmark)
- [ ] `landing_page/index.html` exists
- [ ] `.nojekyll` file exists in `landing_page/`
- [ ] All files are committed and pushed to `main` branch
- [ ] Browser cache is cleared
- [ ] Using correct URL: `https://aritrode29.github.io/SunUrban/`

## Still Not Working?

1. **Check Actions Logs**:
   - Go to Actions tab
   - Click on the latest workflow run
   - Check each step for errors
   - Look for red X marks

2. **Verify File Paths**:
   - All HTML files should use relative paths
   - Example: `href="styles.css"` not `href="/styles.css"`
   - Example: `href="parkurban.html"` not `href="/parkurban.html"`

3. **Check File Permissions**:
   - Make sure files are readable (not in .gitignore)
   - Verify case sensitivity (index.html not Index.html)

4. **Wait Longer**:
   - Sometimes GitHub Pages takes 5-10 minutes to propagate
   - DNS changes can take up to 24 hours (but usually < 5 min)

## Test Locally First

Before deploying, test locally:

```powershell
cd "g:\My Drive\UT_Austin_MSSD\Proposals\MIC_Javad-CAEE\LandingPage_SunnyGrids\landing_page"
python -m http.server 8000
```

Then visit: `http://localhost:8000`

If it works locally but not on GitHub Pages, it's a deployment issue.

## Get Help

If none of the above works:

1. Check GitHub Status: https://www.githubstatus.com/
2. Review GitHub Pages docs: https://docs.github.com/en/pages
3. Check repository settings for any restrictions

---

**Most Common Fix**: Enable GitHub Pages in Settings → Pages → Source: GitHub Actions

