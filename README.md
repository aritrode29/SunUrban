# SunUrban - Urban DER Platform

<div align="center">

🌞 **Transforming Urban Infrastructure into Clean Energy Assets**

[![Deploy to GitHub Pages](https://github.com/aritrode29/SunUrban/actions/workflows/deploy.yml/badge.svg)](https://github.com/aritrode29/SunUrban/actions/workflows/deploy.yml)
[![Website](https://img.shields.io/badge/Website-Live-brightgreen)](https://aritrode29.github.io/SunUrban/)

</div>

---

## 🎯 Overview

**SunUrban** is an integrated urban distributed energy resource (DER) platform that transforms parking lots, EV charging stations, and buildings into coordinated clean energy assets. Our platform combines solar canopies, battery storage, EV charging, and smart parking management into a unified energy ecosystem.

🌐 **Live Website**: [https://aritrode29.github.io/SunUrban/](https://aritrode29.github.io/SunUrban/)

---

## 🚀 Platform Products

### 🅿️ ParkUrban
**Smart Parking Intelligence Platform**

Turn parking infrastructure into a revenue-generating, data-driven asset.

- **Real-time Analytics**: Occupancy, utilization rates, dwell time analysis
- **Peak Time Optimization**: Heatmap visualizations for demand patterns
- **Zone Management**: Distribution analytics by parking zones
- **Revenue Optimization**: Dynamic pricing recommendations
- **Operator Dashboard**: Comprehensive analytics for parking operators

📊 [View ParkUrban Dashboard](https://aritrode29.github.io/SunUrban/parkurban-dashboard.html)  
💰 [View Financial Projections](https://aritrode29.github.io/SunUrban/parkurban-financials.html)

---

### ⚡ ChargeUrban
**Urban EV Charging Network**

Seamless, intelligent EV charging integrated with solar canopy infrastructure.

- **Smart Charging**: AI-optimized charging schedules
- **Solar Integration**: Direct solar-to-vehicle charging
- **V2G Capability**: Vehicle-to-grid services for grid support
- **Mobile App**: Find stations, start sessions, track charging
- **Membership Plans**: Flexible pricing from pay-as-you-go to unlimited

💰 [View Financial Projections](https://aritrode29.github.io/SunUrban/chargeurban-financials.html)

---

### 🔋 GridUrban
**Virtual Power Plant & DER Exchange**

Coordinate distributed energy resources into a unified virtual power plant.

- **DER Aggregation**: Solar, battery, and EV assets coordinated
- **Grid Services**: Frequency regulation, demand response
- **Energy Trading**: Peer-to-peer energy marketplace
- **ERCOT Integration**: Real-time market participation

---

## 📁 Project Structure

```
SunUrban/
│
├── landing_page/                 # Website (Deployed to GitHub Pages)
│   ├── index.html               # Main landing page
│   ├── parkurban.html           # ParkUrban product page
│   ├── chargeurban.html         # ChargeUrban product page
│   ├── gridurban.html           # GridUrban product page
│   ├── parkurban-dashboard.html # Operator analytics dashboard
│   ├── parkurban-financials.html# ParkUrban financial projections
│   ├── chargeurban-financials.html # ChargeUrban financial projections
│   ├── financials.html          # Main financials overview
│   ├── pricing.html             # Platform pricing plans
│   ├── about.html               # Team & company info
│   ├── how-it-works.html        # Platform explanation
│   ├── contact.html             # Contact form
│   ├── data-layer.html          # Data architecture overview
│   ├── energy-dashboard.html    # Energy analytics dashboard
│   ├── pypsa-analysis.html      # PyPSA modeling results
│   ├── join-waitlist.html       # Waitlist signup
│   ├── styles.css               # Global styles
│   └── script.js                # Interactive functionality
│
├── pypsa_models/                 # PyPSA Energy Modeling
│   ├── optimized_scenario_config.py
│   ├── financial_calculator.py
│   ├── run_optimized_pypsa_scenarios.py
│   └── plot_optimized_pypsa_outputs.py
│
├── data_fetchers/                # Data Acquisition
│   ├── nrel_pvwatts_fetcher.py  # NREL PVWatts API
│   └── ercot_data_fetcher.py    # ERCOT price generator
│
├── visualizations/               # Generated Charts
│   └── [PNG visualization files]
│
├── docs/                         # Documentation
│   ├── PARKURBAN_STANDALONE_IMPLEMENTATION.md
│   ├── IRR_COMPREHENSIVE_GUIDE.md
│   ├── CAPEX_ANALYSIS.md
│   └── [other docs]
│
├── .github/workflows/            # CI/CD
│   └── deploy.yml               # GitHub Pages deployment
│
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 📊 Financial Projections

### ParkUrban (B2B SaaS Model)

| Metric | Year 1 | Year 3 | Year 5 |
|--------|--------|--------|--------|
| Parking Lots | 50 | 350 | 1,000 |
| ARR | $360K | $3.78M | $14.4M |
| Gross Margin | 75% | 80% | 85% |
| LTV:CAC | 3.2x | 4.8x | 6.5x |

### ChargeUrban (EV Charging Network)

| Metric | Year 1 | Year 3 | Year 5 |
|--------|--------|--------|--------|
| Charging Stations | 25 | 200 | 750 |
| Revenue | $425K | $5.4M | $26.25M |
| Gross Margin | 35% | 45% | 55% |
| EBITDA Margin | -15% | 18% | 32% |

---

## 🛠️ Technical Stack

### Website
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js for data visualization
- **Deployment**: GitHub Pages with GitHub Actions CI/CD

### Energy Modeling
- **Framework**: PyPSA (Python for Power System Analysis)
- **Data Sources**: NREL PVWatts API, ERCOT market data
- **Optimization**: HiGHS linear programming solver

### Location
- **Target Market**: Austin, TX
- **Coordinates**: 30.27°N, 97.74°W
- **Grid**: ERCOT (Texas Interconnection)

---

## 🚀 Quick Start

### View the Website
Visit: [https://aritrode29.github.io/SunUrban/](https://aritrode29.github.io/SunUrban/)

### Run Locally
```bash
# Clone the repository
git clone https://github.com/aritrode29/SunUrban.git
cd SunUrban

# Open the landing page
# Windows
start landing_page/index.html

# Mac
open landing_page/index.html

# Linux
xdg-open landing_page/index.html
```

### Run PyPSA Analysis
```bash
# Install dependencies
pip install -r requirements.txt

# Set NREL API key
export NREL_API_KEY="your_key_here"  # Linux/Mac
$env:NREL_API_KEY = "your_key_here"  # PowerShell

# Run scenarios
cd pypsa_models
python run_optimized_pypsa_scenarios.py
```

---

## 📈 Key Features

### Platform Features
- ✅ **Integrated Dashboard**: Unified view across all products
- ✅ **Real-time Analytics**: Live data visualization
- ✅ **Financial Modeling**: Detailed 5-year projections
- ✅ **Scenario Analysis**: Multiple business scenarios
- ✅ **Mobile Responsive**: Works on all devices

### Energy Modeling Features
- ✅ **NREL PVWatts Integration**: Real solar generation data
- ✅ **ERCOT Price Patterns**: Realistic wholesale prices
- ✅ **Multi-scenario Optimization**: BTM, Hybrid, VPP, Marketplace
- ✅ **Battery Storage Optimization**: Arbitrage and grid services

---

## 🎓 Academic Context

This project was developed as part of the **MIC Proposal** for:

- **Institution**: University of Texas at Austin
- **Program**: MS Sustainable Design
- **Department**: Civil, Architectural & Environmental Engineering (CAEE)

### Team
- **Kendall Baker** - Project Lead
- **Aritro De** - Technical Lead
- **Jae** - Team Member
- **Tejoo** - Team Member

---

## 📄 License

This project is for academic and research purposes.

---

## 🤝 Contributing

Interested in collaborating? 

- 🐛 [Open an issue](https://github.com/aritrode29/SunUrban/issues)
- 📧 Contact us through the [website contact form](https://aritrode29.github.io/SunUrban/contact.html)

---

## 🙏 Acknowledgments

- **NREL** - PVWatts API and solar resource data
- **PyPSA** - Power system analysis framework
- **ERCOT** - Market data and grid information
- **UT Austin** - Academic support and guidance

---

<div align="center">

**Last Updated**: January 2025  
**Version**: 3.0  
**Status**: ✅ Production Ready

🌞 *Transforming Urban Infrastructure into Clean Energy Assets* 🌞

</div>
