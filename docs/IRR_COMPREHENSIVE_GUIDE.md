# IRR Comprehensive Guide

This guide consolidates all IRR-related documentation including the problem, solutions, optimizer explanation, and improvement strategies.

---

## Table of Contents

1. [The IRR Problem](#the-irr-problem)
2. [IRR Optimizer Overview](#irr-optimizer-overview)
3. [How the Optimizer Works](#how-the-optimizer-works)
4. [Improvement Strategies](#improvement-strategies)
5. [Current Results](#current-results)

---

## The IRR Problem

### Initial Situation
- **PPA Rate**: 9.0¢/kWh (market-competitive for distributed solar)
- **IRR**: **1.9%** (TOO LOW - need 10%+)
- **Payback**: 19.7 years (TOO LONG - need 6-10 years)
- **NPV**: -$2.22M (NEGATIVE)

### The Challenge
- Market-competitive PPA rates are **7-8¢/kWh** (lower than 9¢)
- Lower PPA = less revenue = even lower IRR
- But CAPEX is too high ($4.86M)
- **How do we get to 10% IRR with market-competitive pricing?**

---

## IRR Optimizer Overview

The IRR Optimizer is a tool that automatically finds the **best combination** of:
- PPA rate (price you charge for electricity)
- CAPEX (how much you spend to build the project)
- Battery size (how much storage you install)
- Revenue streams (different ways to make money)

...to achieve your **target IRR of 10% or higher**.

### Key Results

**Best Solution Found: 20.8% IRR** ✅

**Configuration:**
- **PPA Rate**: 7.54¢/kWh (market-competitive)
- **Net CAPEX**: $1.81M (-63% reduction from $4.86M)
- **Total Revenue**: $423k/year
- **IRR**: 20.8% (Target: 10%+) ✅
- **Payback**: 4.8 years ✅
- **NPV**: $2.24M ✅

---

## How the Optimizer Works

### Step 1: PPA + CAPEX Optimization

**What it does:**
- Tests different PPA rates (7.0¢ to 8.0¢/kWh)
- Tests different CAPEX levels ($1.46M to $4.86M)
- Finds the combination that gives exactly 10% IRR

**Result:**
- PPA: 7.54¢/kWh
- CAPEX: $1.81M (-63%)
- IRR: 10.0%

### Step 2: Battery Sizing Optimization

**What it does:**
- Tests different battery configurations (power and duration)
- Finds the best fit within the target CAPEX

**Result:**
- Battery Power: 865 kW (50% of solar)
- Battery Energy: 432 kWh (0.5 hour duration)
- Battery Cost: $0.32M
- IRR: 17.8%

### Step 3: Revenue Streams Optimization

**What it does:**
- Tests different combinations of revenue streams
- Maximizes total revenue while maintaining feasibility

**Result:**
- Base PPA: $243k
- Grid Services: $100k (revised to $60k - battery-based)
- EV Charging: $50k
- REC Sales: $30k
- Platform Fees: $19k
- Digital Twin: $75k
- **Total**: $477k/year

---

## Improvement Strategies

### 1. Increase Revenue (Most Impact)

#### Option A: Higher PPA Rates
- **Current**: 7.54¢/kWh
- **Target**: 12-15¢/kWh
- **Impact**: +33-67% revenue
- **IRR Improvement**: 7.8% → 9-11%
- **Feasibility**: ⭐⭐⭐ High (market-driven)

#### Option B: Add Revenue Streams
- **Grid Services**: $60k/year (battery-based)
- **EV Charging**: $50k/year
- **REC Sales**: $30k/year
- **Platform Fees**: $19k/year
- **Digital Twin**: $75k/year
- **Total Additional**: $234k/year

### 2. Reduce CAPEX

#### Option A: Battery Cost Reduction
- **Current**: $400/kWh
- **Target**: $200/kWh (-50%)
- **Timeline**: 2026-2027 (industry trend)
- **Savings**: ~$1.4M

#### Option B: Optimize Battery Sizing
- **Current**: 0.5h duration
- **Target**: Optimize for specific use case
- **Savings**: Variable

#### Option C: Scale Economies
- **Current**: 3 sites
- **Target**: 10+ sites
- **Savings**: ~$500-700k

### 3. Combined Approach (Best Results)

**Combined: Revenue +50% AND CAPEX -30%**
- **IRR**: **10.6%** ✅
- **Payback**: 8.7 years ✅
- **NPV**: $0.78M (positive) ✅

---

## Current Results

### Final Optimized Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| **PPA Rate** | 7.54¢/kWh | Market-competitive |
| **Net CAPEX** | $4.71M | No ITC |
| **Battery Power** | 865 kW | 50% of solar |
| **Battery Energy** | 433 kWh | 0.5h duration |
| **Total Revenue** | $477k/year | All streams |
| **IRR** | **7.8%** | Without ITC |
| **Payback** | 10.9 years | Without ITC |
| **NPV** | -$0.08M | Almost break-even |

### Revenue Breakdown

| Revenue Stream | Amount | % of Total |
|----------------|--------|------------|
| Base PPA | $243k | 51% |
| Digital Twin Licensing | $75k | 16% |
| Grid Services | $60k | 13% |
| EV Charging | $50k | 10% |
| REC Sales | $30k | 6% |
| Platform Fees | $19k | 4% |
| **Total** | **$477k** | **100%** |

### Investor Appeal

- **Commercial Solar Investors**: ⚠️ BORDERLINE (7.8% < 8% threshold, but close)
- **Infrastructure/ESG Investors**: ✅ YES (7.8% acceptable)

---

## Next Steps

1. ✅ **Optimize battery dispatch** for grid services
2. ✅ **Enroll in ERCOT** ancillary services markets
3. ✅ **Focus on self-consumption** optimization
4. ✅ **Explore additional revenue** streams
5. ⚠️ **Consider capacity expansion** if financially viable

---

**Last Updated**: November 2025  
**Status**: Comprehensive guide consolidated ✅

