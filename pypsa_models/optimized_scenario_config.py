"""
Optimized Scenario Configuration
=================================

Updated scenario parameters based on IRR optimizer results.
This replaces the original scenario assumptions with optimized values.
"""

# Optimized parameters from IRR optimizer
OPTIMIZED_CONFIG = {
    # PPA Rate (optimized from 9.0¢ to 7.54¢/kWh)
    'ppa_rate_cents_per_kwh': 7.54,
    
    # CAPEX (without ITC - actual investment required)
    'net_capex_usd': 4_710_145,  # $4.71M (no ITC credit)
    'capex_reduction_pct': 3.1,  # vs original $4.86M
    
    # Battery Configuration (optimized)
    'battery_config': {
        'power_fraction': 0.5,  # 50% of solar capacity (vs 100% before)
        'duration_hours': 0.5,  # 0.5 hours (vs 2.0 hours before)
        'total_power_kw': 865,  # 50% of 1730 kW
        'total_energy_kwh': 432,  # 865 kW × 0.5h
        'battery_cost_usd': 320_000  # $0.32M (vs $2.77M before)
    },
    
    # Revenue Streams (optimized)
    # NOTE: Grid services revised - battery-based ancillary services + demand response
    # Energy export services NOT feasible (generation < demand)
    # Battery-based services FEASIBLE (frequency regulation, spinning reserve, voltage support)
    # Demand response FEASIBLE (peak load reduction)
    'revenue_streams': {
        'base_ppa': 243_000,  # $243k/year (7.54¢/kWh × 3,219 MWh)
        'platform_fees': 19_000,  # $19k/year (1.5¢/kWh on 40% of generation)
        'grid_services': 60_000,  # $60k/year (battery-based ancillary + demand response, revised from $100k)
        'ev_charging': 50_000,  # $50k/year
        'rec_sales': 30_000,  # $30k/year
        'digital_twin_licensing': 75_000,  # $75k/year (data licensing SaaS - $25k/site)
        'total': 477_000  # $477k/year total (revised grid services: $60k vs original $100k)
    },
    
    # Financial Metrics (without ITC, with Digital Twin, with Revised Grid Services)
    # NOTE: Grid services revised to $60k/year (battery-based + demand response)
    # Based on PyPSA analysis: energy export not feasible, but battery services are
    'financial_metrics': {
        'irr_pct': 7.8,  # Without ITC, with Digital Twin, with Revised Grid Services ($60k)
        'payback_years': 10.9,  # Without ITC, with Digital Twin, with Revised Grid Services
        'npv_usd': -80_000,  # Without ITC, with Digital Twin, with Revised Grid Services
        'annual_cash_flow': 434_000  # Revenue - OPEX = $477k - $43k
    },
    
    # Site-specific battery configurations (optimized)
    'sites': {
        'Site_A': {  # South Congress - 550 kW solar
            'solar_kw': 550,
            'battery_kw': 275,  # 50% of solar (vs 550 kW before)
            'battery_kwh': 138,  # 0.5h duration (vs 1100 kWh before)
        },
        'Site_B': {  # UT Campus - 380 kW solar
            'solar_kw': 380,
            'battery_kw': 190,  # 50% of solar (vs 380 kW before)
            'battery_kwh': 95,  # 0.5h duration (vs 760 kWh before)
        },
        'Site_C': {  # Airport - 800 kW solar
            'solar_kw': 800,
            'battery_kw': 400,  # 50% of solar (vs 800 kW before)
            'battery_kwh': 200,  # 0.5h duration (vs 1600 kWh before)
        }
    },
    
    # Total system
    'total_solar_kw': 1730,
    'total_battery_kw': 865,  # 50% of solar
    'total_battery_kwh': 433,  # 0.5h duration
    
    # Annual generation (unchanged)
    'annual_generation_mwh': 3219,
    
    # OPEX (unchanged)
    'annual_opex_usd': 43_000,
}


# Comparison: Original vs Optimized
COMPARISON = {
    'ppa_rate': {
        'original': 9.0,  # cents/kWh
        'optimized': 7.54,  # cents/kWh
        'change_pct': -16.2
    },
    'net_capex': {
        'original': 4_860_000,  # USD (with ITC)
        'optimized': 4_710_145,  # USD (without ITC)
        'change_pct': -3.1
    },
    'battery_power': {
        'original': 1730,  # kW (100% of solar)
        'optimized': 865,  # kW (50% of solar)
        'change_pct': -50.0
    },
    'battery_energy': {
        'original': 3460,  # kWh (2h duration)
        'optimized': 433,  # kWh (0.5h duration)
        'change_pct': -87.5
    },
    'battery_duration': {
        'original': 2.0,  # hours
        'optimized': 0.5,  # hours
        'change_pct': -75.0
    },
    'annual_revenue': {
        'original': 290_000,  # USD (base PPA only)
        'optimized': 442_000,  # USD (with all streams)
        'change_pct': +52.4
    },
    'irr': {
        'original': 1.9,  # percent (with ITC)
        'optimized': 6.9,  # percent (without ITC)
        'change_pct': +263.2
    },
    'payback': {
        'original': 19.7,  # years (with ITC)
        'optimized': 11.8,  # years (without ITC)
        'change_pct': -40.1
    }
}


def get_optimized_site_config(site_name):
    """
    Get optimized configuration for a specific site.
    
    Parameters:
    -----------
    site_name : str
        Site name ('Site_A', 'Site_B', or 'Site_C')
    
    Returns:
    --------
    dict
        Site configuration with optimized parameters
    """
    if site_name not in OPTIMIZED_CONFIG['sites']:
        raise ValueError(f"Unknown site: {site_name}")
    
    return OPTIMIZED_CONFIG['sites'][site_name].copy()


def get_optimized_capex():
    """
    Get optimized CAPEX value.
    
    Returns:
    --------
    float
        Optimized net CAPEX in USD
    """
    return OPTIMIZED_CONFIG['net_capex_usd']


def get_optimized_ppa_rate():
    """
    Get optimized PPA rate.
    
    Returns:
    --------
    float
        Optimized PPA rate in cents/kWh
    """
    return OPTIMIZED_CONFIG['ppa_rate_cents_per_kwh']


def get_optimized_revenue_streams():
    """
    Get optimized revenue streams.
    
    Returns:
    --------
    dict
        Revenue streams breakdown
    """
    return OPTIMIZED_CONFIG['revenue_streams'].copy()


def print_optimization_summary():
    """
    Print a summary of optimization results.
    """
    print("="*80)
    print("OPTIMIZED SCENARIO CONFIGURATION")
    print("="*80)
    print("\nKey Changes from Original:")
    print("-" * 80)
    
    comp = COMPARISON
    print(f"\n1. PPA Rate:")
    print(f"   Original: {comp['ppa_rate']['original']:.2f}¢/kWh")
    print(f"   Optimized: {comp['ppa_rate']['optimized']:.2f}¢/kWh")
    print(f"   Change: {comp['ppa_rate']['change_pct']:.1f}%")
    
    print(f"\n2. Net CAPEX:")
    print(f"   Original: ${comp['net_capex']['original']/1e6:.2f}M")
    print(f"   Optimized: ${comp['net_capex']['optimized']/1e6:.2f}M")
    print(f"   Change: {comp['net_capex']['change_pct']:.1f}%")
    
    print(f"\n3. Battery Configuration:")
    print(f"   Power: {comp['battery_power']['original']} kW -> {comp['battery_power']['optimized']} kW ({comp['battery_power']['change_pct']:.1f}%)")
    print(f"   Energy: {comp['battery_energy']['original']} kWh -> {comp['battery_energy']['optimized']} kWh ({comp['battery_energy']['change_pct']:.1f}%)")
    print(f"   Duration: {comp['battery_duration']['original']}h -> {comp['battery_duration']['optimized']}h ({comp['battery_duration']['change_pct']:.1f}%)")
    
    print(f"\n4. Annual Revenue:")
    print(f"   Original: ${comp['annual_revenue']['original']/1e3:.0f}k (base PPA only)")
    print(f"   Optimized: ${comp['annual_revenue']['optimized']/1e3:.0f}k (with all streams)")
    print(f"   Change: {comp['annual_revenue']['change_pct']:.1f}%")
    
    print(f"\n5. Financial Metrics:")
    print(f"   IRR: {comp['irr']['original']:.1f}% -> {comp['irr']['optimized']:.1f}% ({comp['irr']['change_pct']:.1f}% improvement)")
    print(f"   Payback: {comp['payback']['original']:.1f} years -> {comp['payback']['optimized']:.1f} years ({comp['payback']['change_pct']:.1f}% improvement)")
    
    print("\n" + "="*80)
    print("Revenue Streams Breakdown:")
    print("-" * 80)
    rev = OPTIMIZED_CONFIG['revenue_streams']
    print(f"  Base PPA: ${rev['base_ppa']/1e3:.0f}k")
    print(f"  Platform Fees: ${rev['platform_fees']/1e3:.0f}k")
    print(f"  Grid Services: ${rev['grid_services']/1e3:.0f}k (REVISED - battery-based + demand response)")
    print(f"  EV Charging: ${rev['ev_charging']/1e3:.0f}k")
    print(f"  REC Sales: ${rev['rec_sales']/1e3:.0f}k")
    print(f"  Digital Twin Licensing: ${rev.get('digital_twin_licensing', 0)/1e3:.0f}k")
    print(f"  Total: ${rev['total']/1e3:.0f}k")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print_optimization_summary()

