# SunUrban Landing Page

This is the SunUrban landing page website, deployed via GitHub Pages.

## Structure

- `index.html` - Main landing page
- `parkurban.html` - ParkUrban product page
- `gridurban.html` - GridUrban product page
- `about.html` - About/Team page
- `how-it-works.html` - How it Works page
- `pricing.html` - Pricing page
- `contact.html` - Contact page
- `financials.html` - Financials page
- `parkurban-financials.html` - ParkUrban Financial Projections
- `chargeurban-financials.html` - ChargeUrban Financial Projections
- `parkurban-dashboard.html` - ParkUrban Operator Dashboard
- `data-layer.html` - Data Layer analysis page
- `energy-dashboard.html` - Energy Dashboard page
- `pypsa-analysis.html` - PyPSA Analysis page
- `styles.css` - Main stylesheet
- `script.js` - Main JavaScript file

## Deployment

This site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch.

The deployment workflow is configured in `.github/workflows/deploy.yml`.

## Local Development

Simply open `index.html` in a web browser or use a local server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve
```

Then navigate to `http://localhost:8000` in your browser.





