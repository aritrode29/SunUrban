"""
Run Optimized CAPEX Analysis
============================

Updates CAPEX analysis with optimized parameters and creates visualization.
"""

import sys
sys.path.insert(0, 'pypsa_models')

from optimized_scenario_config import (
    OPTIMIZED_CONFIG, get_optimized_capex, get_optimized_revenue_streams
)
from capex_analysis import calculate_site_capex, calculate_financial_metrics, plot_capex_breakdown

def run_optimized_capex_analysis():
    """
    Run CAPEX analysis with optimized parameters.
    """
    print("="*80)
    print("OPTIMIZED CAPEX ANALYSIS")
    print("="*80)
    
    # Get optimized site configurations
    sites = OPTIMIZED_CONFIG['sites']
    
    # Calculate CAPEX for each site with optimized battery sizes
    site_capex_data = {}
    total_capex = 0
    
    for site_name, config in sites.items():
        capex = calculate_site_capex(
            config['solar_kw'],
            config['battery_kw'],
            config['battery_kwh']
        )
        site_capex_data[site_name] = capex
        total_capex += capex['net_capex']
    
    print("\nSite Configurations (Optimized):")
    print("-" * 80)
    for site_name, config in sites.items():
        print(f"\n{site_name}:")
        print(f"  Solar: {config['solar_kw']} kW")
        print(f"  Battery: {config['battery_kw']} kW / {config['battery_kwh']} kWh")
        print(f"  Net CAPEX: ${site_capex_data[site_name]['net_capex']/1e6:.2f}M")
    
    print(f"\nTotal System:")
    print(f"  Solar: {OPTIMIZED_CONFIG['total_solar_kw']} kW")
    print(f"  Battery: {OPTIMIZED_CONFIG['total_battery_kw']} kW / {OPTIMIZED_CONFIG['total_battery_kwh']} kWh")
    print(f"  Total Net CAPEX: ${total_capex/1e6:.2f}M")
    
    # Revenue streams
    revenue_streams = get_optimized_revenue_streams()
    annual_revenue = revenue_streams['total']
    annual_opex = OPTIMIZED_CONFIG['annual_opex_usd']
    net_capex = get_optimized_capex()
    
    # Calculate financial metrics
    metrics = calculate_financial_metrics(
        annual_revenue, annual_opex, net_capex,
        25, 0.08
    )
    
    print("\n" + "="*80)
    print("OPTIMIZED FINANCIAL METRICS")
    print("="*80)
    print(f"\n  Net CAPEX: ${net_capex/1e6:.2f}M")
    print(f"  Annual Revenue: ${annual_revenue/1e3:.0f}k")
    print(f"  Annual OPEX: ${annual_opex/1e3:.0f}k")
    print(f"  Annual Cash Flow: ${metrics['annual_cash_flow']/1e3:.0f}k")
    print(f"\n  IRR: {metrics['irr']*100:.1f}%")
    print(f"  Payback: {metrics['payback_years']:.1f} years")
    print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
    print(f"  ROI: {metrics['roi']:.1f}%")
    
    # Prepare analysis structure for visualization
    s1_metrics = calculate_financial_metrics(
        revenue_streams['base_ppa'], annual_opex, net_capex, 25, 0.08
    )
    
    total_capex_sum = sum(s['total_capex'] for s in site_capex_data.values())
    total_net_capex_sum = sum(s['net_capex'] for s in site_capex_data.values())
    total_solar_mw = OPTIMIZED_CONFIG['total_solar_kw'] / 1000
    
    analysis = {
        'aggregate': {
            'total_capex': total_capex_sum,
            'net_capex': net_capex,
            'total_net_capex': total_net_capex_sum,
            'total_solar_kw': OPTIMIZED_CONFIG['total_solar_kw'],
            'total_battery_kw': OPTIMIZED_CONFIG['total_battery_kw'],
            'total_battery_kwh': OPTIMIZED_CONFIG['total_battery_kwh'],
            'total_opex': annual_opex,
            'cost_per_kw': total_capex_sum / OPTIMIZED_CONFIG['total_solar_kw'],
            'cost_per_mw': total_capex_sum / total_solar_mw
        },
        'sites': site_capex_data,
        'scenarios': {
            'S1_BTM_PPA': {
                'net_capex': net_capex,
                'annual_revenue': revenue_streams['base_ppa'],
                'annual_opex': annual_opex,
                'annual_cash_flow': s1_metrics['annual_cash_flow'],
                'irr': s1_metrics['irr'],
                'payback_years': s1_metrics['payback_years'],
                'npv': s1_metrics['npv']
            },
            'S4_Marketplace': {
                'net_capex': net_capex,
                'annual_revenue': annual_revenue,
                'annual_opex': annual_opex,
                'annual_cash_flow': metrics['annual_cash_flow'],
                'irr': metrics['irr'],
                'payback_years': metrics['payback_years'],
                'npv': metrics['npv']
            }
        }
    }
    
    print("\n" + "="*80)
    print("CREATING OPTIMIZED CAPEX VISUALIZATION...")
    print("="*80)
    
    # Create visualization
    plot_capex_breakdown(analysis, save_path='visualizations/optimized_capex_analysis.png')
    
    print("\n" + "="*80)
    print("OPTIMIZED CAPEX ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  [CHART] visualizations/optimized_capex_analysis.png")
    
    return analysis


if __name__ == "__main__":
    analysis = run_optimized_capex_analysis()

