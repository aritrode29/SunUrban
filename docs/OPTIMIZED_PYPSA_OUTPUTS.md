# Optimized PyPSA Outputs Documentation

## Overview

This document describes the comprehensive PyPSA scenario analysis outputs generated with optimized parameters. The analysis includes detailed visualizations of loads, generation, battery operation, optimization results, and financial metrics.

---

## Generated Visualizations

### 1. **Comprehensive PyPSA Outputs** (`optimized_pypsa_comprehensive.png`)

A 16-panel comprehensive visualization showing:

#### **Generation & Load Analysis**
- **Solar Generation Profiles**: Hourly generation from each canopy site (Site A, B, C)
- **Host Load Profiles**: Hourly load profiles for each site
- **Generation vs Load Balance**: Surplus/deficit analysis throughout the day
- **Battery Operation (Power)**: Charge/discharge profiles for each battery
- **Battery State of Charge**: SOC trajectories throughout the day

#### **Grid Interaction**
- **Grid Import/Export**: Hourly grid interaction showing when energy is imported or exported
- **Energy Flow (Stacked)**: Stacked visualization showing all energy sources meeting load

#### **Financial Analysis**
- **Revenue vs Costs by Scenario**: Comparison of revenue and costs for each scenario
- **Revenue Breakdown**: Detailed breakdown of PPA and grid revenue
- **Battery Energy Throughput**: Total energy charged/discharged per battery

#### **System Configuration**
- **Energy Balance Summary**: Total generation, load, surplus, deficit, self-consumption rate
- **System Configuration Summary**: Optimized system parameters (solar, battery, PPA rate, CAPEX)
- **Financial Metrics Summary**: IRR, payback, NPV, ROI with all revenue streams

---

### 2. **Load Analysis** (`optimized_pypsa_loads.png`)

A detailed 9-panel load analysis visualization:

#### **Load Profiles**
- **Individual Site Load Profiles**: Hourly load for each site (Site A, B, C)
- **Total System Load Profile**: Aggregated load profile
- **Load Statistics**: Peak, average, minimum, and daily totals for each site

#### **Load Characteristics**
- **Load Duration Curve**: Load ranked from highest to lowest
- **Load-Generation Match Quality**: Hourly match ratio between generation and load
- **Stacked Load Profiles**: Visual breakdown of load by site

#### **Load Metrics**
- **Peak Load Hour**: Hour of day with maximum load
- **System Load Factor**: Average load / peak load ratio
- **Total Daily Load Energy**: Total energy consumption in MWh

---

### 3. **Optimization Details** (`optimized_pypsa_optimization.png`)

A detailed 9-panel optimization analysis:

#### **Optimization Strategy**
- **Hourly System Cost**: Cost breakdown by hour (grid import costs)
- **Battery Optimization Strategy**: Battery arbitrage (charge low, discharge high)
- **Power Balance**: Supply (generation + battery + grid) vs demand (load)

#### **Optimization Results**
- **Scenario Comparison**: Total revenue vs net revenue by scenario
- **Battery Utilization**: Average utilization percentage for each battery
- **Energy Flow Summary**: Detailed breakdown of energy sources and uses

#### **Optimization Metrics**
- **Self-Consumption Rate**: Percentage of generation consumed on-site
- **Grid Independence**: Percentage of load met without grid import
- **Optimization Cost Savings**: Savings vs naive dispatch strategy

---

## Optimized Parameters Used

### System Configuration
- **Solar Capacity**: 1,730 kW total
  - Site A: 550 kW
  - Site B: 380 kW
  - Site C: 800 kW

- **Battery Capacity**: 865 kW / 433 kWh total (50% power, 0.5h duration)
  - Site A: 275 kW / 138 kWh
  - Site B: 190 kW / 95 kWh
  - Site C: 400 kW / 200 kWh

- **PPA Rate**: 7.54¢/kWh (optimized)

- **Net CAPEX**: $4.71M (no ITC)

### Revenue Streams
- **Base PPA**: $243k/year
- **Platform Fees**: $19k/year
- **Grid Services**: $100k/year
- **EV Charging**: $50k/year
- **REC Sales**: $30k/year
- **Digital Twin Licensing**: $75k/year
- **Total**: $517k/year

### Financial Metrics
- **IRR**: 8.9%
- **Payback**: 9.9 years
- **NPV**: $0.35M
- **ROI**: 10.0%

---

## Scenario Results

### Scenario 1: BTM PPA (Optimized)
- **Generation**: 8,870.7 kWh/day
- **Load**: 14,480.0 kWh/day
- **PPA Revenue**: $668.85/day
- **Grid Revenue**: $282.69/day
- **Net Revenue**: $951.54/day

### Scenario 2: Hybrid PPA + Grid Sales (Optimized)
- **Generation**: 8,903.2 kWh/day
- **Load**: 14,480.0 kWh/day
- **PPA Revenue**: $671.30/day
- **Grid Revenue**: $208.68/day
- **Net Revenue**: $879.98/day

---

## Key Insights

### 1. **Battery Optimization**
- Batteries are optimized for **arbitrage** (charge during low-price hours, discharge during high-price hours)
- With **0.5h duration**, batteries provide short-term smoothing and peak shaving
- **50% power capacity** reduces CAPEX while maintaining flexibility

### 2. **Load-Generation Balance**
- **Self-consumption rate**: ~60-65% (generation consumed on-site)
- **Grid independence**: ~40-45% (load met without grid import)
- **Surplus generation**: Available for grid export or battery charging

### 3. **Optimization Benefits**
- **Cost savings**: Optimization reduces system costs by managing battery dispatch optimally
- **Revenue maximization**: Batteries enable selling during high-price hours
- **Grid interaction**: Optimal balance between self-consumption and grid sales

### 4. **Financial Performance**
- **IRR**: 8.9% (above 8% threshold for commercial solar investors)
- **Payback**: 9.9 years (reasonable for infrastructure investment)
- **NPV**: $0.35M (positive, indicating value creation)

---

## Technical Details

### PyPSA Optimization
- **Solver**: HiGHS (open-source linear programming solver)
- **Objective**: Minimize system cost (grid import costs - grid export revenue)
- **Constraints**: 
  - Power balance at each bus
  - Battery energy balance
  - Battery power limits
  - Battery energy capacity limits
  - Transmission line limits

### Network Topology
- **Buses**: HOUSTON, NORTH, SOUTH, WEST, GRID
- **Transmission Lines**: 4 lines (800-2000 MW capacity)
- **Grid Connection**: Bidirectional link to GRID bus (10 MW capacity)

### Time Resolution
- **Snapshots**: 24 hours (hourly resolution)
- **Date**: June 15, 2024 (typical summer day)

---

## Usage

### Running the Analysis

```bash
python run_optimized_pypsa.py
```

This will:
1. Create optimized PyPSA networks
2. Run LOPF optimization for each scenario
3. Generate comprehensive visualizations
4. Output results to `visualizations/` folder

### Output Files

1. `optimized_pypsa_comprehensive.png` - 16-panel comprehensive analysis
2. `optimized_pypsa_loads.png` - 9-panel load analysis
3. `optimized_pypsa_optimization.png` - 9-panel optimization details

---

## Interpretation Guide

### Reading the Visualizations

1. **Generation Profiles**: Show when solar is producing (typically 6 AM - 8 PM)
2. **Load Profiles**: Show when hosts consume energy (varies by site type)
3. **Battery Operation**: 
   - Positive = discharging (supplying power)
   - Negative = charging (consuming power)
4. **Grid Interaction**:
   - Positive = exporting to grid
   - Negative = importing from grid
5. **State of Charge**: Battery energy level (0-100%)

### Key Metrics to Watch

- **Self-Consumption Rate**: Higher = less grid dependency
- **Battery Utilization**: Higher = better battery ROI
- **Grid Independence**: Higher = more resilient system
- **Optimization Savings**: Higher = better optimization performance

---

## Next Steps

1. **Annual Analysis**: Extend to full year with seasonal variations
2. **Sensitivity Analysis**: Test impact of parameter changes
3. **Market Price Integration**: Use real ERCOT LMP data
4. **Multiple Scenarios**: Add more business model scenarios
5. **Grid Services**: Model frequency regulation, demand response

---

**Last Updated**: November 2025  
**Status**: Complete ✅

