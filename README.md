# Urban DER Exchange - PyPSA Modeling Project

## 🎯 Project Overview

This project models an **Urban Distributed Energy Resource (DER) Exchange** for solar canopy installations in Austin, TX. It uses PyPSA (Python for Power System Analysis) to optimize energy dispatch across multiple scenarios with **real NREL solar data** and **ERCOT market prices**.

## 📁 Project Structure

```
LandingPage_SunnyGrids/
│
├── pypsa_models/              # Main PyPSA scenario analysis
│   ├── optimized_scenario_config.py       # Optimized configuration
│   ├── financial_calculator.py            # Unified financial calculations
│   ├── run_optimized_pypsa_scenarios.py  # PyPSA scenario runner
│   ├── plot_optimized_pypsa_outputs.py   # Comprehensive visualizations
│   └── [other analysis modules]           # Additional analysis modules
│
├── data_fetchers/             # Data acquisition modules
│   ├── nrel_pvwatts_fetcher.py           # NREL PVWatts API client
│   ├── nrel_data_fetcher.py              # NREL NSRDB API client (legacy)
│   └── ercot_data_fetcher.py             # ERCOT LMP price generator
│
├── visualizations/            # Generated charts and figures
│   ├── pypsa_der_exchange_topology.png
│   ├── pypsa_der_exchange_comparison.png
│   ├── pypsa_der_exchange_dispatch_S1-S4.png
│   ├── pypsa_der_exchange_marketplace.png
│   └── der_exchange_analysis.png
│
├── docs/                      # Documentation
│   ├── IRR_COMPREHENSIVE_GUIDE.md        # Complete IRR optimization guide
│   ├── CAPEX_ANALYSIS.md                 # Cost breakdown and assumptions
│   ├── BATTERY_OPTIMIZATION.md           # Battery optimization methodology
│   ├── PRICING_MECHANISMS.md             # Pricing algorithms
│   ├── OPTIMIZED_PYPSA_OUTPUTS.md        # PyPSA analysis results
│   ├── REVISED_GRID_SERVICES.md          # Grid services analysis
│   ├── DIGITAL_TWIN_LICENSING.md         # Digital Twin revenue stream
│   └── [other analysis docs]             # Additional analysis documents
│
├── archive/                   # Archived/superseded files
│   └── [archived files]                   # Legacy and superseded files
│
├── landing_page/              # Web presentation
│   └── [landing page files]              # HTML, CSS, JS, images
│
├── visualizations/            # Generated charts and figures
│   └── [PNG visualization files]         # All analysis visualizations
│
├── PROJECT_SUMMARY.md         # Comprehensive project summary
├── CONSOLIDATION_SUMMARY.md   # File consolidation summary
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Get NREL API key (free)
# Visit: https://developer.nrel.gov/signup/
```

### 2. Set API Key

```powershell
# PowerShell
$env:NREL_API_KEY = "your_key_here"
```

### 3. Run Analysis

```bash
cd pypsa_models
python pypsa_der_exchange_scenarios.py
```

This will:
- ✅ Fetch real NREL PVWatts solar data for Austin, TX
- ✅ Generate realistic ERCOT LMP prices
- ✅ Run 5 scenarios with PyPSA optimization
- ✅ Create 7 high-quality visualizations

## 📊 Scenarios Modeled

### Scenario 0: Baseline
- No solar canopies
- All power from grid at retail rate
- **Cost**: $2,268/day

### Scenario 1: Behind-the-Meter PPA
- Solar serves hosts only, no grid export
- Fixed PPA rate (9¢/kWh)
- **Revenue**: $794/day | **Annual (3 sites)**: $290k

### Scenario 2: Hybrid (PPA + Grid Sales)
- Solar serves hosts + exports surplus to grid
- Battery storage for arbitrage
- **Revenue**: $721/day | **Annual (3 sites)**: $263k

### Scenario 3: VPP / DER Exchange
- Coordinated dispatch across all sites
- Grid services + demand response
- **Revenue**: $721/day | **Annual (3 sites)**: $263k

### Scenario 4: Community Solar Marketplace ⭐
- Energy block trading (10 kWh blocks)
- Dynamic pricing (7-15¢/kWh)
- Platform exchange fee (1.5¢/kWh)
- **Revenue**: $529/day | **Platform margin**: $57/day
- **Annual (50 sites)**: $3.2M total, $1M in platform fees

## 💰 Revenue Projections

| Scenario | Daily (3 sites) | Annual (3 sites) | Annual (50 sites) |
|----------|----------------|------------------|-------------------|
| S1: BTM PPA | $794 | $290k | $4.8M |
| S2: Hybrid | $721 | $263k | $4.4M |
| S3: VPP | $721 | $263k | $4.4M |
| **S4: Marketplace** | **$529** | **$193k** | **$3.2M** |

## 📈 Key Features

### Real Data Integration
- ✅ **NREL PVWatts API**: Actual solar generation profiles
- ✅ **ERCOT Patterns**: Realistic wholesale prices
- ✅ **Austin, TX Location**: Specific lat/lon (30.27°N, 97.74°W)
- ✅ **Validated Performance**: 21.2% capacity factor (June)

### PyPSA Optimization
- ✅ **4-bus ERCOT network** (Houston, North, South, West)
- ✅ **3 solar sites** (550 kW, 380 kW, 800 kW)
- ✅ **Battery storage** (2 hours at each site)
- ✅ **HiGHS solver** (linear programming)
- ✅ **24-hour dispatch** optimization

### Visualizations
1. Network topology diagram
2. Scenario comparison (5 scenarios)
3. Dispatch schedules (4 scenarios)
4. Marketplace trading details

## 🔧 Technical Details

### Network Components
- **Buses**: 4 (HOUSTON, NORTH, SOUTH, WEST)
- **Transmission Lines**: 4 (1000-2000 MW capacity)
- **Solar Generators**: 3 canopy sites
- **Battery Storage**: 3 units (2-hour duration)
- **Loads**: On-site host loads + marketplace consumers

### Optimization
- **Solver**: HiGHS (open-source LP solver)
- **Objective**: Minimize system cost
- **Constraints**: Power balance, transmission limits, battery SOC
- **Resolution**: Hourly (24 snapshots)

### Data Sources
- **Solar**: NREL PVWatts API v8
- **Prices**: Synthetic ERCOT LMP ($15-1,131/MWh)
- **Loads**: Typical commercial/residential patterns

## 📚 Documentation

### Main Docs
- [`docs/README_DER_Exchange.md`](docs/README_DER_Exchange.md) - Full technical documentation
- [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) - Data sources and validation
- [`docs/README_NREL_Integration.md`](docs/README_NREL_Integration.md) - NREL API guide

### Code Documentation
All Python modules include comprehensive docstrings and inline comments.

## 🗂️ Archive

The `archive/` folder contains earlier versions of the model:
- **urban_der_exchange.py**: Original simplified model with synthetic data
- **urban_der_exchange_with_nrel.py**: NSRDB API version (deprecated)
- **urban_der_exchange_with_pvwatts.py**: First PVWatts integration
- **demo_with_sample_nrel_data.py**: Demo with realistic synthetic profiles

These are kept for reference but are superseded by the PyPSA models.

## 🌐 Landing Page

The `landing_page/` folder contains a professional web presentation:
- Interactive dashboard mockup
- Scenario descriptions
- Team information
- Contact forms

Open `landing_page/Landing-Page_SolarCanopy.html` in a browser.

## 🔄 Workflow

### Standard Analysis Run

```bash
# 1. Set API key
$env:NREL_API_KEY = "your_key_here"

# 2. Run scenarios
cd pypsa_models
python pypsa_der_exchange_scenarios.py

# 3. View outputs
cd ../visualizations
# Open PNG files to view results
```

### Custom Scenarios

Edit `pypsa_models/pypsa_der_exchange_scenarios.py` to:
- Modify site capacities
- Change PPA rates
- Adjust battery sizing
- Add new consumer types
- Modify pricing algorithms

## 📦 Dependencies

```
pypsa>=0.26.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
requests>=2.28.0
```

See `requirements.txt` for complete list.

## 🎓 Academic Context

This project was developed as part of the MIC Proposal for:
- **Institution**: University of Texas at Austin
- **Program**: MS Sustainable Design
- **Course**: MIC - Javad (CAEE)
- **Team**: Kendall Baker, Aritro De

## 📝 Citation

If you use this model in your research, please cite:

```
Urban DER Exchange - PyPSA Modeling Framework
University of Texas at Austin, 2025
https://github.com/[your-repo]
```

## 🤝 Contributing

This is an academic project. For questions or collaboration:
- Open an issue on GitHub
- Contact: [your contact info]

## 📄 License

This project is for academic and research purposes.

## 🙏 Acknowledgments

- **NREL** for PVWatts API and solar resource data
- **PyPSA** team for the power system analysis framework
- **ERCOT** for market data and grid information
- **UT Austin** for academic support

---

**Last Updated**: November 2025  
**Version**: 2.0 (PyPSA Implementation)  
**Status**: ✅ Production Ready

