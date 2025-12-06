# Battery Optimization in PyPSA

## Overview

Yes, **batteries are fully optimized** in the PyPSA model using **Linear Optimal Power Flow (LOPF)** optimization. The optimization automatically determines the optimal charge/discharge schedule to minimize system costs while respecting all physical and economic constraints.

## How PyPSA Optimizes Batteries

### 1. **Optimization Framework**

PyPSA uses **Linear Programming (LP)** with the **HiGHS solver** to optimize battery dispatch. The optimization:

- **Objective Function**: Minimize total system cost
  - Cost of grid purchases (at LMP prices)
  - Revenue from grid sales (at LMP prices)
  - PPA revenue (fixed rate)
  - Battery operation costs (minimal, mainly efficiency losses)

- **Decision Variables**: 
  - Battery charge power (p_store) at each hour
  - Battery discharge power (p_dispatch) at each hour
  - State of charge (SOC) at each hour

### 2. **Battery Constraints**

The optimization enforces these physical constraints:

#### **Energy Balance (State of Charge)**
```
SOC[t+1] = SOC[t] + (η_charge × p_store[t] - p_dispatch[t]/η_discharge) × Δt - losses
```

Where:
- `SOC[t]` = State of charge at time t
- `η_charge` = Charging efficiency (95%)
- `η_discharge` = Discharging efficiency (95%)
- `p_store[t]` = Power charging battery (MW)
- `p_dispatch[t]` = Power discharging from battery (MW)
- `losses` = Standing losses (0.01% per hour)

#### **Power Limits**
```
0 ≤ p_store[t] ≤ p_nom        (max charge rate)
0 ≤ p_dispatch[t] ≤ p_nom      (max discharge rate)
```

Where `p_nom` = rated power capacity:
- Site A: 550 kW
- Site B: 380 kW  
- Site C: 800 kW

#### **Energy Capacity Limits**
```
0 ≤ SOC[t] ≤ e_nom            (max energy capacity)
```

Where `e_nom` = energy capacity (2 hours duration):
- Site A: 1,100 kWh (2 × 550 kW)
- Site B: 760 kWh (2 × 380 kW)
- Site C: 1,600 kWh (2 × 800 kW)

#### **Initial/Final State**
```
SOC[0] = initial_SOC          (typically 0 or 50%)
SOC[24] = final_SOC           (can be free or constrained)
```

### 3. **Optimization Strategy**

The optimizer automatically determines battery dispatch to:

#### **Arbitrage Opportunities**
- **Charge** when prices are low (excess solar, low LMP)
- **Discharge** when prices are high (peak demand, high LMP)
- Maximize revenue from price differences

#### **Load Shifting**
- Store excess solar generation during midday
- Discharge during evening peak when solar is low
- Reduce grid purchases at high prices

#### **Grid Services**
- Provide flexibility for grid balancing
- Support local load during peak hours
- Enable grid export when profitable

### 4. **Battery Parameters in Model**

Based on the documentation (`docs/DATA_SOURCES.md`):

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Round-trip efficiency** | 90% | 95% charge × 95% discharge |
| **Standing loss** | 0.01%/hour | Self-discharge rate |
| **Duration** | 2 hours | Energy capacity / power rating |
| **Cyclic operation** | Daily | Can fully charge/discharge each day |

### 5. **Example Optimization Logic**

The optimizer considers:

```
For each hour t:
  1. Available solar generation
  2. Local load demand
  3. Grid LMP price
  4. Battery current SOC
  5. Battery capacity limits
  
Decision:
  - If (solar > load) AND (LMP is low):
      → Charge battery (store excess solar)
  
  - If (solar < load) AND (LMP is high):
      → Discharge battery (avoid expensive grid purchase)
  
  - If (LMP is very high) AND (battery has energy):
      → Discharge to grid (sell at high price)
```

### 6. **Optimization Outputs**

After optimization, PyPSA provides:

- **`n.storage_units_t.p`**: Net power (positive = discharge, negative = charge)
- **`n.storage_units_t.state_of_charge`**: Energy stored at each hour
- **`n.storage_units_t.p_store`**: Charging power
- **`n.storage_units_t.p_dispatch`**: Discharging power

### 7. **Visualization**

The battery optimization results are visualized in:
- **`visualizations/pypsa_der_exchange_dispatch_S2.png`** (Hybrid scenario)
- **`visualizations/pypsa_der_exchange_dispatch_S3.png`** (VPP scenario)
- **`visualizations/pypsa_der_exchange_dispatch_S4.png`** (Marketplace scenario)

These show:
- Battery charge/discharge schedule
- State of charge over 24 hours
- Coordination with solar generation

## Key Benefits of Optimization

1. **Maximizes Revenue**: Optimizes arbitrage between low/high prices
2. **Minimizes Costs**: Reduces expensive grid purchases
3. **Physical Feasibility**: Ensures all constraints are satisfied
4. **Economic Efficiency**: Finds globally optimal solution
5. **Real-time Dispatch**: Provides hour-by-hour schedule

## Technical Details

### Solver
- **HiGHS**: Open-source linear programming solver
- **Method**: Dual simplex algorithm
- **Solution**: Globally optimal (LP is convex)

### Computational Complexity
- **Variables**: ~72 per battery (24 hours × 3 variables)
- **Constraints**: ~96 per battery (energy balance + limits)
- **Solve Time**: < 1 second for full 24-hour optimization

### Optimization Type
- **Linear Programming (LP)**: All constraints and objective are linear
- **Deterministic**: Same inputs → same optimal solution
- **Convex**: Guaranteed global optimum

## Summary

**Yes, batteries are fully optimized** using PyPSA's LOPF framework. The optimization:

✅ Minimizes total system cost  
✅ Maximizes revenue from arbitrage  
✅ Respects all physical constraints  
✅ Provides optimal charge/discharge schedule  
✅ Coordinates with solar and grid prices  

The optimization is **automatic** - you just define the battery parameters and constraints, and PyPSA finds the optimal dispatch schedule that maximizes economic value while ensuring physical feasibility.

---

**References:**
- PyPSA Documentation: https://pypsa.readthedocs.io/
- HiGHS Solver: https://highs.dev/
- Battery Storage Database: https://www.nrel.gov/grid/battery-storage.html

