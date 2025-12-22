# SunUrban

Urban DER (Distributed Energy Resource) platform and MIC proposal codebase.

## Overview

This repository contains two main pieces:

- **Public-facing landing site** (deployed via GitHub Pages) describing ParkUrban, ChargeUrban, and GridUrban.
- **Energy modeling + analysis stack** built around PyPSA and NREL/ERCOT data for the Urban DER Exchange concept.

Live site: `https://aritrode29.github.io/SunUrban/`

## Repository Structure

- **`landing_page/`**: All HTML/CSS/JS for the website (what GitHub Pages serves)
  - `index.html` – main SunUrban landing page
  - `parkurban.html`, `chargeurban.html`, `gridurban.html` – product pages
  - `parkurban-dashboard.html` – operator analytics mock dashboard
  - `parkurban-financials.html`, `chargeurban-financials.html` – 5-year projections
  - `financials.html`, `pricing.html`, `about.html`, `how-it-works.html`, `contact.html`, `data-layer.html`, `energy-dashboard.html`, `pypsa-analysis.html`, `join-waitlist.html`
  - `styles.css`, `script.js`
- **`pypsa_models/`**: PyPSA-based modeling of the Urban DER Exchange
  - `run_optimized_pypsa_scenarios.py`, `optimized_scenario_config.py`, `financial_calculator.py`, `plot_optimized_pypsa_outputs.py`
- **`data_fetchers/`**: NREL PVWatts + ERCOT-style data utilities
- **`visualizations/`**: Generated plots and figures
- **`docs/`**: Written documentation (MIC proposal support, financials, implementation notes)
- **`.github/workflows/deploy.yml`**: GitHub Actions workflow deploying `landing_page/` to GitHub Pages
- **`requirements.txt`**: Python dependencies for the modeling stack

## How to View the Site

- Hosted: `https://aritrode29.github.io/SunUrban/`
- Local preview:
  - Clone the repo
  - Open `landing_page/index.html` in a browser (no build step required)

```bash
git clone https://github.com/aritrode29/SunUrban.git
cd SunUrban

# Windows
start landing_page/index.html

# macOS
open landing_page/index.html

# Linux
xdg-open landing_page/index.html
```

## How to Run the PyPSA Models

```bash
pip install -r requirements.txt

# set NREL key (example)
export NREL_API_KEY="your_key_here"      # bash/zsh
# or in PowerShell:
# $env:NREL_API_KEY = "your_key_here"

cd pypsa_models
python run_optimized_pypsa_scenarios.py
```

This will run the configured scenarios and write results/plots into `visualizations/`.

## Product Concepts (High Level)

- **ParkUrban** – parking analytics + operator tooling (utilization, dwell time, peak periods, zone distribution, financial projections).
- **ChargeUrban** – EV charging network + pricing/membership model, integrated with the DER/solar concept.
- **GridUrban** – DER exchange / virtual power plant framing, backed by the PyPSA modeling work.

The website in `landing_page/` is a narrative + product-style wrapper around these concepts and the modeling work in this repo.

## Tech Stack (Brief)

- **Frontend**: HTML, CSS, vanilla JS, Chart.js for charts
- **Modeling**: Python, PyPSA, numpy/pandas/matplotlib
- **Data**: NREL PVWatts, ERCOT-style price traces (via helper scripts)
- **Deployment**: GitHub Pages via GitHub Actions (`deploy.yml`)

## Academic Context

Built as part of a MIC proposal at UT Austin (CAEE / MS Sustainable Design) to explore urban DER exchanges, solar canopies, and parking/EV integration in Austin, TX.

## License / Use

This repository is intended for academic, research, and proposal-support use. If you reuse or adapt components, please preserve attribution and context where possible.

