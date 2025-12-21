# Quick Fix: Site Not Opening

## ✅ FIXED: CSS and JS Files

I've copied `styles.css` and `script.js` from `assets/` to the root of `landing_page/` so they can be found by the HTML files.

## Next Steps to Get Site Working

### 1. Enable GitHub Pages (CRITICAL!)

**This is likely why nothing is opening!**

1. Go to: **https://github.com/aritrode29/SunUrban/settings/pages**
2. Under **"Source"**, select: **"GitHub Actions"**
3. Click **"Save"**
4. Wait 1-2 minutes

### 2. Check Deployment Status

1. Go to: **https://github.com/aritrode29/SunUrban/actions**
2. Look for **"Deploy to GitHub Pages"** workflow
3. Check if it's:
   - ✅ **Green** = Success (wait 2-3 min for site to be live)
   - ⏳ **Yellow** = In progress (wait)
   - ❌ **Red** = Failed (check error logs)

### 3. Visit Your Site

After enabling GitHub Pages and workflow completes:
- **URL**: https://aritrode29.github.io/SunUrban/
- Wait 2-3 minutes after enabling
- Clear browser cache (Ctrl+Shift+R)

### 4. If Still Not Working

**Check Actions Logs:**
1. Go to Actions tab
2. Click on latest workflow run
3. Check each step for errors
4. Look for red X marks

**Common Issues:**
- ❌ "Environment not found" → Create `github-pages` environment in Settings → Environments
- ❌ "Permission denied" → Settings → Actions → General → Enable "Read and write permissions"
- ❌ "No such file" → Verify `landing_page/index.html` exists

## Files Now in Place

✅ `landing_page/index.html`  
✅ `landing_page/styles.css` (copied from assets/)  
✅ `landing_page/script.js` (copied from assets/)  
✅ `.github/workflows/deploy.yml`  
✅ `landing_page/.nojekyll`  

## Test Locally First

To verify files work before deploying:

```powershell
cd "g:\My Drive\UT_Austin_MSSD\Proposals\MIC_Javad-CAEE\LandingPage_SunnyGrids\landing_page"
python -m http.server 8000
```

Then visit: `http://localhost:8000`

If it works locally but not on GitHub Pages, it's a deployment/enablement issue.

---

**Most Likely Issue**: GitHub Pages is not enabled in repository settings!
