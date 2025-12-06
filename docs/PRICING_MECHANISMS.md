# Pricing Mechanisms in the DER Exchange Model

## Overview

The model uses **three different pricing mechanisms** depending on the scenario and energy source:

1. **ERCOT LMP (Locational Marginal Price)** - Grid wholesale prices
2. **Exchange/Marketplace Prices** - Dynamic supply/demand pricing
3. **PPA (Power Purchase Agreement) Prices** - Fixed contract rates

---

## 1. ERCOT LMP Prices (Grid Wholesale)

### Source
- **Primary**: Real ERCOT data via `gridstatus` package (if available)
- **Fallback**: Synthetic prices based on historical ERCOT patterns

### Implementation
Located in: `data_fetchers/ercot_data_fetcher.py`

### How It Works

#### Real Data (if `gridstatus` installed):
```python
ercot = ERCOT()
lmp_data = ercot.get_lmp(
    date=start_date,
    end=end_date,
    market='REAL_TIME_15_MIN',
    location_type='Hub',
    locations='HB_HOUSTON'
)
# Resampled to hourly
```

#### Synthetic Data (fallback):
Based on typical ERCOT patterns:

```python
base_price = 35.0  # $/MWh

# Time-of-day multipliers:
if 16 <= hour <= 20:  # Peak (4-8 PM)
    price = base_price × random(2.5, 4.0)  # $87.50 - $140/MWh
    
elif 10 <= hour <= 15:  # Mid-day (solar rich)
    price = base_price × random(0.6, 1.2)  # $21 - $42/MWh
    
elif 2 <= hour <= 6:  # Off-peak
    price = base_price × random(0.5, 0.8)  # $17.50 - $28/MWh
    
else:  # Normal hours
    price = base_price × random(0.9, 1.5)  # $31.50 - $52.50/MWh

# Add volatility
price *= normal(1.0, 0.15)  # ±15% random variation

# Occasional spikes (5% chance)
if random() < 0.05:
    price *= random(3, 10)  # 3-10x multiplier

# Floor at $15/MWh
price = max(15.0, price)
```

### Price Characteristics

| Time Period | Typical Range | Description |
|-------------|---------------|-------------|
| **Peak (4-8 PM)** | $87-140/MWh | High demand, low solar |
| **Mid-day (10 AM-3 PM)** | $21-42/MWh | Solar generation peak |
| **Off-peak (2-6 AM)** | $17-28/MWh | Low demand |
| **Normal hours** | $31-52/MWh | Moderate demand |
| **Price spikes** | $500-9,000/MWh | Rare scarcity events |

### Usage in Model
- **Grid imports**: Marginal cost = LMP price
- **Grid exports**: Revenue = LMP price
- **Battery arbitrage**: Optimizes charge/discharge based on LMP

---

## 2. Exchange/Marketplace Prices (Dynamic)

### Source
**Dynamic algorithm** based on real-time supply/demand balance

### Implementation
Function: `calculate_exchange_price(supply_kw, demand_kw)`

### How It Works

The price is determined by the **supply-to-demand ratio**:

```python
ratio = supply_kw / max(demand_kw, 1.0)

if ratio >= 1.5:
    price = 7.0  # ¢/kWh (excess supply)
    
elif ratio >= 1.0:
    price = 7.0 + (15.0 - 7.0) × 0.3  # = 9.4¢/kWh
    
elif ratio >= 0.7:
    price = 7.0 + (15.0 - 7.0) × 0.6  # = 11.8¢/kWh
    
else:  # ratio < 0.7
    price = 7.0 + (15.0 - 7.0) × 0.9  # = 14.2¢/kWh
```

### Price Formula

```
Price = Base_Price + (Retail_Price - Base_Price) × Multiplier

Where:
- Base_Price = 7¢/kWh (when excess supply)
- Retail_Price = 15¢/kWh (Austin Energy typical rate)
- Multiplier = f(supply/demand_ratio)
```

### Price Tiers

| Supply/Demand Ratio | Price (¢/kWh) | Condition |
|---------------------|---------------|-----------|
| **≥ 1.5** | **7.0¢** | Excess supply (surplus solar) |
| **1.0 - 1.5** | **9.4¢** | Balanced supply/demand |
| **0.7 - 1.0** | **11.8¢** | Moderate deficit |
| **< 0.7** | **14.2¢** | High deficit (near retail) |

### Example Scenarios

**Midday (11 AM)** - High solar, low demand:
- Supply: 1,200 kW
- Demand: 500 kW
- Ratio: 2.4
- **Price: 7.0¢/kWh** (excess supply)

**Evening (6 PM)** - Low solar, high demand:
- Supply: 200 kW
- Demand: 1,200 kW
- Ratio: 0.17
- **Price: 14.2¢/kWh** (high deficit)

**Afternoon (3 PM)** - Moderate solar, moderate demand:
- Supply: 800 kW
- Demand: 850 kW
- Ratio: 0.94
- **Price: 11.8¢/kWh** (slight deficit)

### Price Cap
- **Maximum**: 15¢/kWh (retail rate)
- **Minimum**: 7¢/kWh (base price)

### Usage in Model
- **Scenario 4 (Marketplace)**: Energy block trading at exchange prices
- **Consumer savings**: Difference between exchange price and retail (15¢/kWh)
- **Platform revenue**: Exchange fee (1.5¢/kWh) on top of energy price

---

## 3. PPA (Power Purchase Agreement) Prices

### Source
**Fixed contract rate** - Long-term agreement between solar owner and host

### Implementation
Fixed rate defined in scenario functions

### How It Works

**Fixed Rate**: **9¢/kWh** (typical commercial PPA rate)

This is a **long-term contract** where:
- Solar owner sells energy to host at fixed rate
- Rate is lower than retail (15¢/kWh) but higher than wholesale
- Provides price stability for both parties

### Price Characteristics

| Parameter | Value | Description |
|-----------|-------|-------------|
| **PPA Rate** | 9¢/kWh | Fixed contract price |
| **Retail Rate** | 15¢/kWh | What host would pay otherwise |
| **Host Savings** | 6¢/kWh | Difference (40% savings) |
| **Contract Term** | 20-25 years | Typical PPA duration |

### Usage in Model
- **Scenario 1 (BTM PPA)**: All solar sold to hosts at 9¢/kWh
- **Scenario 2 (Hybrid)**: Host load served at 9¢/kWh, surplus to grid at LMP
- **Revenue calculation**: `PPA_revenue = energy_to_hosts × 9¢/kWh`

---

## Price Comparison

### Typical Hourly Prices (June Day)

| Hour | LMP ($/MWh) | Exchange (¢/kWh) | PPA (¢/kWh) | Retail (¢/kWh) |
|------|-------------|------------------|-------------|----------------|
| 2 AM | $20 | 14.2 | 9.0 | 15.0 |
| 11 AM | $25 | 7.0 | 9.0 | 15.0 |
| 3 PM | $30 | 9.4 | 9.0 | 15.0 |
| 6 PM | $100 | 14.2 | 9.0 | 15.0 |
| 9 PM | $50 | 14.2 | 9.0 | 15.0 |

### Price Relationships

```
Wholesale (LMP) < PPA < Exchange < Retail

Typical ranges:
- LMP: $20-140/MWh (2-14¢/kWh)
- PPA: 9¢/kWh (fixed)
- Exchange: 7-14.2¢/kWh (dynamic)
- Retail: 15¢/kWh (fixed)
```

---

## How Prices Drive Optimization

### Battery Optimization
- **Charge** when LMP is low (midday solar surplus)
- **Discharge** when LMP is high (evening peak)
- **Arbitrage** = Revenue from price differences

### Solar Dispatch
- **Serve hosts** at PPA rate (9¢/kWh) - guaranteed revenue
- **Export to grid** at LMP - variable but potentially higher
- **Marketplace** at exchange price - dynamic, supply/demand driven

### Revenue Maximization
The PyPSA optimizer automatically chooses:
1. **When to charge batteries** (low LMP)
2. **When to discharge** (high LMP)
3. **Where to send solar** (hosts vs grid vs marketplace)
4. **Optimal dispatch** to maximize total revenue

---

## Data Sources & Validation

### ERCOT LMP
- **Real data**: ERCOT Public Reports, `gridstatus` package
- **Synthetic**: Based on historical ERCOT patterns (2020-2023)
- **Validation**: Matches typical ERCOT ranges ($15-1,131/MWh)

### Exchange Prices
- **Algorithm**: Supply/demand ratio-based
- **Validation**: Similar to time-of-use (TOU) rates
- **Reference**: Austin Energy TOU rates, dynamic pricing models

### PPA Prices
- **Source**: Typical commercial PPA rates (2023-2024)
- **Validation**: Industry standard 8-10¢/kWh for commercial
- **Reference**: NREL PPA price database

---

## Summary

| Price Type | Range | Variability | Usage |
|------------|-------|-------------|-------|
| **LMP** | $15-1,131/MWh | High (hourly) | Grid transactions |
| **Exchange** | 7-14.2¢/kWh | Medium (supply/demand) | Marketplace trading |
| **PPA** | 9¢/kWh | None (fixed) | Host contracts |
| **Retail** | 15¢/kWh | None (fixed) | Consumer reference |

**Key Insight**: The model uses **multiple pricing mechanisms** to reflect real-world energy markets, where different transactions occur at different price points based on contracts, market conditions, and supply/demand balance.

---

**References:**
- ERCOT Market Information: http://www.ercot.com/mktinfo
- Austin Energy Rates: https://austinenergy.com/ae/rates
- NREL PPA Price Database: https://www.nrel.gov/grid/solar-ppa-prices.html
- EIA Electricity Prices: https://www.eia.gov/electricity/monthly/

