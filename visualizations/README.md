# Visualizations

This folder contains all generated charts and figures from the PyPSA scenario analysis.

## Generated Files

### 1. Network Topology
- **File**: `pypsa_der_exchange_topology.png`
- **Description**: 4-bus ERCOT network with 3 solar canopy sites
- **Shows**: Buses, transmission lines, capacities, geographic layout

### 2. Scenario Comparison
- **File**: `pypsa_der_exchange_comparison.png`
- **Description**: Comprehensive comparison of all 5 scenarios
- **Charts**:
  - Daily revenue by scenario
  - Net benefit comparison
  - Generation mix (solar vs grid)
  - Revenue breakdown by source
  - Annual projection (3 sites)
  - Scaling projection (3 vs 50 sites)

### 3. Dispatch Schedules
- **Files**: 
  - `pypsa_der_exchange_dispatch_S1.png` (BTM PPA)
  - `pypsa_der_exchange_dispatch_S2.png` (Hybrid)
  - `pypsa_der_exchange_dispatch_S3.png` (VPP)
  - `pypsa_der_exchange_dispatch_S4.png` (Marketplace)
- **Description**: 24-hour dispatch optimization results
- **Shows**:
  - Generation sources (stacked)
  - Load vs generation balance
  - Battery operation (charge/discharge)
  - Battery state of charge

### 4. Marketplace Trading
- **File**: `pypsa_der_exchange_marketplace.png`
- **Description**: Detailed analysis of energy block trading
- **Shows**:
  - Supply vs marketplace demand
  - Dynamic exchange pricing
  - Energy block trades timeline
  - Trade economics by consumer
  - Revenue breakdown
  - Cumulative energy traded
  - Platform economics summary

## Specifications

- **Format**: PNG
- **Resolution**: 300 DPI (publication quality)
- **Color Scheme**: Consistent across all charts

## Regenerating

To regenerate all visualizations:

```bash
cd ../pypsa_models
python pypsa_der_exchange_scenarios.py
```

---

**Auto-generated**: During PyPSA scenario analysis  
**Quality**: Publication-ready

