"""
Financial Metrics Calculator
============================

Unified utility for calculating and displaying financial metrics with various scenarios.
"""

import sys
sys.path.insert(0, 'pypsa_models')

from optimized_scenario_config import (
    OPTIMIZED_CONFIG, get_optimized_revenue_streams, get_optimized_capex
)
from capex_analysis import calculate_financial_metrics


def calculate_current_metrics():
    """
    Calculate current financial metrics from optimized configuration.
    """
    rev = get_optimized_revenue_streams()
    capex = get_optimized_capex()
    annual_opex = OPTIMIZED_CONFIG['annual_opex_usd']
    
    metrics = calculate_financial_metrics(rev['total'], annual_opex, capex, 25, 0.08)
    
    return {
        'revenue': rev,
        'capex': capex,
        'opex': annual_opex,
        'metrics': metrics
    }


def print_financial_summary(title="CURRENT FINANCIAL METRICS", comparison=None):
    """
    Print comprehensive financial summary.
    
    Parameters:
    -----------
    title : str
        Title for the summary
    comparison : dict, optional
        Dictionary with 'before' metrics for comparison
    """
    data = calculate_current_metrics()
    rev = data['revenue']
    metrics = data['metrics']
    
    print("="*80)
    print(title)
    print("="*80)
    
    print(f"\nRevenue Breakdown:")
    print(f"  Base PPA: ${rev['base_ppa']/1e3:.0f}k")
    print(f"  Platform Fees: ${rev['platform_fees']/1e3:.0f}k")
    print(f"  Grid Services: ${rev['grid_services']/1e3:.0f}k (battery-based + demand response)")
    print(f"  EV Charging: ${rev['ev_charging']/1e3:.0f}k")
    print(f"  REC Sales: ${rev['rec_sales']/1e3:.0f}k")
    print(f"  Digital Twin Licensing: ${rev.get('digital_twin_licensing', 0)/1e3:.0f}k")
    print(f"  Total: ${rev['total']/1e3:.0f}k/year")
    
    print(f"\nFinancial Metrics:")
    print(f"  Net CAPEX: ${data['capex']/1e6:.2f}M (No ITC)")
    print(f"  Annual Revenue: ${rev['total']/1e3:.0f}k")
    print(f"  Annual OPEX: ${data['opex']/1e3:.0f}k")
    print(f"  Annual Cash Flow: ${metrics['annual_cash_flow']/1e3:.0f}k")
    print(f"  IRR: {metrics['irr']*100:.1f}%")
    print(f"  Payback: {metrics['payback_years']:.1f} years")
    print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
    print(f"  ROI: {metrics['roi']:.1f}%")
    
    if comparison:
        print(f"\nComparison vs Previous:")
        print(f"  Revenue: ${comparison['revenue_before']/1e3:.0f}k -> ${rev['total']/1e3:.0f}k ({((rev['total']-comparison['revenue_before'])/comparison['revenue_before']*100):+.1f}%)")
        print(f"  IRR: {comparison['irr_before']*100:.1f}% -> {metrics['irr']*100:.1f}% ({metrics['irr']*100-comparison['irr_before']*100:+.1f} pp)")
        print(f"  Payback: {comparison['payback_before']:.1f} -> {metrics['payback_years']:.1f} years ({metrics['payback_years']-comparison['payback_before']:+.1f} years)")
        print(f"  NPV: ${comparison['npv_before']/1e6:.2f}M -> ${metrics['npv']/1e6:.2f}M ({metrics['npv']-comparison['npv_before']:+.2f}M)")
    
    print(f"\nInvestor Appeal:")
    if metrics['irr'] >= 0.08:
        print(f"  Commercial Solar Investors: YES ({metrics['irr']*100:.1f}% >= 8%)")
    else:
        print(f"  Commercial Solar Investors: BORDERLINE ({metrics['irr']*100:.1f}% < 8%)")
    print(f"  Infrastructure/ESG Investors: {'YES' if metrics['irr'] >= 0.06 else 'BORDERLINE'} ({metrics['irr']*100:.1f}% {'acceptable' if metrics['irr'] >= 0.06 else 'below typical threshold'})")
    
    print("\n" + "="*80)
    
    return data


def calculate_scenario(scenario_name, revenue_adjustment=0, capex_adjustment=0):
    """
    Calculate metrics for a specific scenario.
    
    Parameters:
    -----------
    scenario_name : str
        Name of the scenario
    revenue_adjustment : float
        Adjustment to total revenue (in USD)
    capex_adjustment : float
        Adjustment to CAPEX (in USD)
    """
    data = calculate_current_metrics()
    rev = data['revenue'].copy()
    capex = data['capex'] + capex_adjustment
    annual_opex = data['opex']
    
    rev['total'] = rev['total'] + revenue_adjustment
    
    metrics = calculate_financial_metrics(rev['total'], annual_opex, capex, 25, 0.08)
    
    print(f"\n{scenario_name}:")
    print(f"  Revenue: ${rev['total']/1e3:.0f}k")
    print(f"  CAPEX: ${capex/1e6:.2f}M")
    print(f"  IRR: {metrics['irr']*100:.1f}%")
    print(f"  Payback: {metrics['payback_years']:.1f} years")
    print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
    
    return metrics


if __name__ == "__main__":
    # Print current metrics
    print_financial_summary()
    
    # Example scenarios
    print("\n" + "="*80)
    print("SCENARIO ANALYSIS")
    print("="*80)
    
    print("\nConservative Grid Services ($40k):")
    calculate_scenario("Conservative", revenue_adjustment=-20_000)
    
    print("\nOptimistic Grid Services ($80k):")
    calculate_scenario("Optimistic", revenue_adjustment=20_000)

