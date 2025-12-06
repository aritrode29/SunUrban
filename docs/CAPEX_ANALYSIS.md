# CAPEX Analysis Documentation

## Overview

This document describes the Capital Expenditure (CAPEX) analysis for the Urban DER Exchange solar canopy installations with battery storage.

## Cost Assumptions

Based on NREL ATB (Annual Technology Baseline) and industry standards for commercial solar canopy systems:

### Component Costs

| Component | Cost | Unit | Description |
|-----------|------|------|-------------|
| **Solar PV** | $1,200 | per kW | Panels + mounting structure |
| **Battery Power** | $800 | per kW | Power capacity (inverter, BMS) |
| **Battery Energy** | $400 | per kWh | Energy capacity (cells) |
| **Inverter** | $150 | per kW | DC/AC inverters |
| **Electrical** | $200 | per kW | Wiring, transformers, switchgear |
| **Installation** | $250 | per kW | Labor, commissioning |
| **Engineering** | $100 | per kW | Design, permits, engineering |
| **Contingency** | 10% | of subtotal | Project contingency |

### Financial Assumptions

| Parameter | Value | Description |
|-----------|-------|-------------|
| **ITC Rate** | 30% | Federal Investment Tax Credit (Section 48) |
| **Project Lifetime** | 25 years | Typical solar system lifetime |
| **Discount Rate** | 8% | For NPV calculations |
| **Annual OPEX** | $25 | per kW/year | Operations & maintenance |

## System Configuration

### Site Capacities

| Site | Solar (kW) | Battery Power (kW) | Battery Energy (kWh) |
|------|------------|-------------------|---------------------|
| Site A (SoCo) | 550 | 550 | 1,100 |
| Site B (Campus) | 380 | 380 | 760 |
| Site C (Airport) | 800 | 800 | 1,600 |
| **Total** | **1,730** | **1,730** | **3,460** |

## CAPEX Breakdown

### Total System CAPEX

- **Total CAPEX (before ITC)**: ~$6.95M
- **ITC Credit (30%)**: ~$2.08M
- **Net CAPEX (after ITC)**: ~$4.86M
- **Cost per kW**: ~$4,015/kW
- **Cost per MW**: ~$4.0M/MW

### Component Breakdown (3 Sites Total)

| Component | Cost | % of Total |
|-----------|------|------------|
| Solar PV | $2.08M | 30% |
| Battery | $2.77M | 40% |
| Inverter | $520k | 7% |
| Electrical | $346k | 5% |
| Installation | $433k | 6% |
| Engineering | $173k | 2% |
| Contingency | $695k | 10% |

## Financial Metrics

### By Scenario

| Scenario | Annual Revenue | Payback | IRR | NPV (25yr) |
|----------|---------------|---------|-----|------------|
| S1: BTM PPA | $290k | 19.7 years | 1.9% | -$2.23M |
| S2: Hybrid | $263k | 22.1 years | 1.0% | -$2.52M |
| S3: VPP | $263k | 22.1 years | 1.0% | -$2.52M |
| S4: Marketplace | $193k | 32.5 years | 0.0% | -$3.26M |

### Key Insights

1. **Best Scenario**: S1 (BTM PPA) has highest IRR (1.9%) and shortest payback (19.7 years)
2. **NPV Negative**: All scenarios show negative NPV at 8% discount rate, indicating:
   - Revenue may need to be higher
   - Costs may need to be lower
   - Or discount rate may be too high for this risk profile
3. **Payback Periods**: 20-33 years, longer than typical 6-8 year target
   - May need higher revenue streams
   - Or lower CAPEX assumptions

## Cost Comparison

### Industry Benchmarks

- **Utility-scale solar**: $800-1,200/kW
- **Commercial rooftop**: $1,500-2,500/kW
- **Solar canopy (this model)**: $4,015/kW
  - Higher due to:
    - Structural requirements (canopy mounting)
    - Battery storage included
    - Urban installation costs
    - Engineering/permits

### Cost Reduction Opportunities

1. **Scale economies**: Larger installations reduce $/kW
2. **Standardization**: Modular designs reduce engineering costs
3. **Battery costs**: Declining rapidly (currently $400/kWh, target $100/kWh)
4. **Installation efficiency**: Learning curve reduces labor costs

## Annual OPEX

- **Total Annual OPEX**: $43k/year (3 sites)
- **Per kW**: $25/kW/year
- **Components**:
  - O&M: $15/kW/year
  - Monitoring: $5/kW/year
  - Insurance: $3/kW/year
  - Other: $2/kW/year

## Sensitivity Analysis

### Key Variables

1. **Revenue**: ±20% change in revenue → ±25% change in NPV
2. **CAPEX**: ±10% change in CAPEX → ±15% change in NPV
3. **ITC**: 30% ITC vs 0% ITC → $2.08M difference
4. **Discount Rate**: 6% vs 8% → +$500k NPV difference

## Recommendations

1. **Revenue Enhancement**:
   - Explore higher PPA rates
   - Add grid services revenue
   - Increase marketplace participation

2. **Cost Reduction**:
   - Optimize battery sizing
   - Standardize designs
   - Negotiate better component pricing

3. **Financial Structure**:
   - Leverage tax credits fully
   - Consider project financing
   - Explore grants/subsidies

## Files Generated

- **`visualizations/capex_analysis.png`**: Comprehensive 8-panel visualization
  - CAPEX breakdown by component
  - CAPEX by site (before/after ITC)
  - Financial metrics comparison
  - NPV analysis
  - Cost per kW comparison
  - Cash flow projections
  - Revenue vs CAPEX
  - Summary table

## Usage

Run standalone CAPEX analysis:
```bash
python run_capex_analysis.py
```

Or integrate with scenario results:
```python
from pypsa_models.capex_analysis import analyze_all_sites_capex

analysis = analyze_all_sites_capex(site_capacities, annual_revenues)
```

## References

- NREL ATB: https://atb.nrel.gov/
- LBNL Solar Cost Database: https://emp.lbl.gov/solar-cost-database
- EIA Capital Costs: https://www.eia.gov/outlooks/aeo/

---

**Last Updated**: November 2025  
**Version**: 1.0

