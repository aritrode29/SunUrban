"""
Run Optimized Scenarios
=======================

Updates all scenario analyses with optimized parameters from IRR optimizer.
"""

import sys
sys.path.insert(0, 'pypsa_models')

from optimized_scenario_config import (
    OPTIMIZED_CONFIG, COMPARISON, 
    print_optimization_summary,
    get_optimized_site_config,
    get_optimized_capex,
    get_optimized_ppa_rate,
    get_optimized_revenue_streams
)
from capex_analysis import calculate_financial_metrics

def update_capex_analysis():
    """
    Update CAPEX analysis with optimized parameters.
    """
    print("="*80)
    print("UPDATING CAPEX ANALYSIS WITH OPTIMIZED PARAMETERS")
    print("="*80)
    
    # Get optimized values
    optimized_capex = get_optimized_capex()
    revenue_streams = get_optimized_revenue_streams()
    annual_revenue = revenue_streams['total']
    annual_opex = OPTIMIZED_CONFIG['annual_opex_usd']
    
    # Calculate financial metrics
    metrics = calculate_financial_metrics(
        annual_revenue, annual_opex, optimized_capex,
        project_lifetime=25, discount_rate=0.08
    )
    
    print("\nOptimized Financial Metrics:")
    print("-" * 80)
    print(f"  Net CAPEX: ${optimized_capex/1e6:.2f}M")
    print(f"  Annual Revenue: ${annual_revenue/1e3:.0f}k")
    print(f"  Annual OPEX: ${annual_opex/1e3:.0f}k")
    print(f"  Annual Cash Flow: ${metrics['annual_cash_flow']/1e3:.0f}k")
    print(f"\n  IRR: {metrics['irr']*100:.1f}%")
    print(f"  Payback: {metrics['payback_years']:.1f} years")
    print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
    
    return metrics


def update_site_configurations():
    """
    Print updated site configurations.
    """
    print("\n" + "="*80)
    print("UPDATED SITE CONFIGURATIONS")
    print("="*80)
    
    sites = OPTIMIZED_CONFIG['sites']
    
    for site_name, config in sites.items():
        print(f"\n{site_name}:")
        print(f"  Solar: {config['solar_kw']} kW")
        print(f"  Battery Power: {config['battery_kw']} kW (50% of solar)")
        print(f"  Battery Energy: {config['battery_kwh']} kWh (0.5h duration)")
    
    print(f"\nTotal System:")
    print(f"  Solar: {OPTIMIZED_CONFIG['total_solar_kw']} kW")
    print(f"  Battery Power: {OPTIMIZED_CONFIG['total_battery_kw']} kW")
    print(f"  Battery Energy: {OPTIMIZED_CONFIG['total_battery_kwh']} kWh")


def update_revenue_breakdown():
    """
    Print updated revenue breakdown.
    """
    print("\n" + "="*80)
    print("UPDATED REVENUE BREAKDOWN")
    print("="*80)
    
    rev = get_optimized_revenue_streams()
    
    print("\nRevenue Streams:")
    print(f"  Base PPA (7.54¢/kWh): ${rev['base_ppa']/1e3:.0f}k ({rev['base_ppa']/rev['total']*100:.1f}%)")
    print(f"  Platform Fees: ${rev['platform_fees']/1e3:.0f}k ({rev['platform_fees']/rev['total']*100:.1f}%)")
    print(f"  Grid Services: ${rev['grid_services']/1e3:.0f}k ({rev['grid_services']/rev['total']*100:.1f}%)")
    print(f"  EV Charging: ${rev['ev_charging']/1e3:.0f}k ({rev['ev_charging']/rev['total']*100:.1f}%)")
    print(f"  REC Sales: ${rev['rec_sales']/1e3:.0f}k ({rev['rec_sales']/rev['total']*100:.1f}%)")
    print(f"\n  Total Revenue: ${rev['total']/1e3:.0f}k")


if __name__ == "__main__":
    # Print optimization summary
    print_optimization_summary()
    
    # Update CAPEX analysis
    metrics = update_capex_analysis()
    
    # Update site configurations
    update_site_configurations()
    
    # Update revenue breakdown
    update_revenue_breakdown()
    
    print("\n" + "="*80)
    print("OPTIMIZATION COMPLETE!")
    print("="*80)
    print("\nAll scenarios should now use:")
    print("  - PPA Rate: 7.54¢/kWh (optimized)")
    print(f"  - Net CAPEX: ${get_optimized_capex()/1e6:.2f}M (optimized, NO ITC)")
    print("  - Battery: 50% power, 0.5h duration (optimized)")
    print(f"  - Revenue: ${get_optimized_revenue_streams()['total']/1e3:.0f}k/year with all streams (optimized, includes Digital Twin)")
    metrics = calculate_financial_metrics(
        get_optimized_revenue_streams()['total'],
        OPTIMIZED_CONFIG['annual_opex_usd'],
        get_optimized_capex(),
        25, 0.08
    )
    print(f"  - IRR: {metrics['irr']*100:.1f}% (optimized, NO ITC)")
    print("\nSee 'pypsa_models/optimized_scenario_config.py' for full configuration.")

