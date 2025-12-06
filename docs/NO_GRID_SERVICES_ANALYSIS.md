# No Grid Services Analysis

## Overview

**Grid services revenue has been removed** from the financial model because **generation is lower than demand**, making it impossible to provide grid services (which require excess generation capacity to export to the grid).

---

## Why Grid Services Cannot Be Provided

### Generation vs Demand

| Metric | Value |
|--------|-------|
| **Annual Generation** | 3,219 MWh/year |
| **Annual Demand** | ~5,280 MWh/year (estimated) |
| **Surplus/Deficit** | **-2,061 MWh/year (DEFICIT)** |

### Daily Analysis

From PyPSA optimization results:
- **Daily Generation**: ~8,900 kWh/day
- **Daily Load**: ~14,480 kWh/day
- **Daily Deficit**: ~5,580 kWh/day

**Conclusion**: System is **net importer** from grid, not exporter. Cannot provide grid services.

---

## What Are Grid Services?

Grid services typically include:
- **Frequency Regulation**: Rapid response to grid frequency deviations
- **Voltage Support**: Maintaining grid voltage within acceptable limits
- **Spinning Reserve**: Standby capacity available for dispatch
- **Peak Shaving**: Reducing grid demand during peak hours

**All require excess generation capacity** to export to the grid.

---

## Impact of Removing Grid Services

### Revenue Impact

| Metric | With Grid Services | Without Grid Services | Change |
|--------|-------------------|----------------------|--------|
| **Base PPA** | $243k | $243k | - |
| **Platform Fees** | $19k | $19k | - |
| **Grid Services** | $100k | **$0k** | **-$100k** |
| **EV Charging** | $50k | $50k | - |
| **REC Sales** | $30k | $30k | - |
| **Digital Twin** | $75k | $75k | - |
| **Total Revenue** | **$517k** | **$417k** | **-$100k** |

### Financial Metrics Impact

| Metric | With Grid Services | Without Grid Services | Change |
|--------|-------------------|----------------------|--------|
| **IRR** | 8.9% | **6.2%** | **-2.7 pp** |
| **Payback** | 9.9 years | **12.6 years** | **+2.7 years** |
| **NPV** | $0.35M | **-$0.72M** | **-$1.07M** |
| **Annual Cash Flow** | $474k | **$374k** | **-$100k** |

### Investor Appeal

| Investor Type | With Grid Services | Without Grid Services |
|---------------|-------------------|----------------------|
| **Commercial Solar** | ✅ YES (8.9% >= 8%) | ⚠️ BORDERLINE (6.2% < 8%) |
| **Infrastructure/ESG** | ✅ YES | ✅ YES (6.2% acceptable) |

---

## Alternative Revenue Strategies

Since grid services are not feasible, focus should shift to:

### 1. **Self-Consumption Optimization**
- Maximize on-site consumption of solar generation
- Reduce grid import costs
- **Potential Savings**: $50-100k/year (depending on retail rates)

### 2. **Battery Arbitrage**
- Charge batteries during low-price hours (night)
- Discharge during high-price hours (peak)
- **Potential Revenue**: $20-50k/year (depending on price spread)

### 3. **Demand Response**
- Reduce load during peak hours (grid pays for load reduction)
- **Potential Revenue**: $10-30k/year (depending on program)

### 4. **Time-of-Use Optimization**
- Shift load to low-price hours
- Use batteries to avoid high-price hours
- **Potential Savings**: $30-60k/year

### 5. **Behind-the-Meter Services**
- Provide services to host (not grid)
- Load shifting, peak shaving for host
- **Potential Revenue**: $20-40k/year (from host)

---

## Revised Revenue Streams

### Current Revenue (Without Grid Services)

| Revenue Stream | Amount | % of Total |
|----------------|--------|------------|
| **Base PPA** | $243k | 58% |
| **Digital Twin Licensing** | $75k | 18% |
| **EV Charging** | $50k | 12% |
| **REC Sales** | $30k | 7% |
| **Platform Fees** | $19k | 5% |
| **Grid Services** | $0k | 0% |
| **Total** | **$417k** | **100%** |

### Potential Additional Revenue

| Source | Potential | Notes |
|--------|-----------|-------|
| **Battery Arbitrage** | $20-50k | Requires price spread |
| **Demand Response** | $10-30k | Requires participation |
| **Behind-the-Meter Services** | $20-40k | Requires host agreement |
| **Time-of-Use Savings** | $30-60k | Indirect (cost reduction) |
| **Total Potential** | **$80-180k** | **Additional revenue** |

**If all potential revenue is realized:**
- **Total Revenue**: $497-597k/year
- **IRR**: 7.5-9.5%
- **Payback**: 10.5-8.5 years
- **NPV**: -$0.2M to +$0.5M

---

## Recommendations

### Short-Term (Year 1-2)
1. ✅ **Remove grid services** from financial projections
2. ✅ **Focus on self-consumption** optimization
3. ✅ **Implement battery arbitrage** (if price spread exists)
4. ✅ **Explore demand response** programs

### Medium-Term (Year 3-5)
1. **Add behind-the-meter services** for hosts
2. **Expand EV charging** infrastructure
3. **Increase Digital Twin** customer base
4. **Optimize time-of-use** strategies

### Long-Term (Year 5+)
1. **Consider expanding solar** capacity (if feasible)
2. **Add more battery** capacity (if cost-effective)
3. **Develop new revenue streams** (e.g., microgrid services)

---

## Conclusion

**Removing grid services** reduces IRR from 8.9% to 6.2%, making the project **borderline** for commercial solar investors but still **acceptable** for infrastructure/ESG investors.

**Key Takeaways:**
- ✅ Grid services are **not feasible** with current generation < demand
- ⚠️ IRR drops to **6.2%** (below 8% threshold)
- ✅ **Alternative revenue streams** can partially offset the loss
- ✅ Project still **viable** with focus on self-consumption and other streams

**Next Steps:**
1. Update all financial models to remove grid services
2. Focus on self-consumption optimization
3. Explore alternative revenue streams
4. Consider expanding capacity if financially viable

---

**Last Updated**: November 2025  
**Status**: Grid services removed from model ✅

