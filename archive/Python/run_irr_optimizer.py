"""
IRR Optimizer Runner
====================

Runs comprehensive optimization to find optimal configuration for 10%+ IRR.
"""

import sys
sys.path.insert(0, 'pypsa_models')

from irr_optimizer import IRROptimizer, plot_optimization_results

if __name__ == "__main__":
    print("="*80)
    print("IRR OPTIMIZER")
    print("="*80)
    print("\nFinding optimal configuration for 10%+ IRR")
    print("while maintaining market-competitive PPA rates...")
    
    # Initialize optimizer
    optimizer = IRROptimizer(target_irr=0.10)
    
    print("\n" + "="*80)
    print("RUNNING OPTIMIZATION...")
    print("="*80)
    
    # Run comprehensive optimization
    results = optimizer.comprehensive_optimization()
    
    print("\n" + "="*80)
    print("OPTIMIZATION RESULTS")
    print("="*80)
    
    # PPA + CAPEX optimization
    sol1 = results['ppa_capex_optimization']
    print("\n1. PPA + CAPEX Optimization:")
    print(f"   PPA Rate: {sol1['ppa_rate']:.2f}¢/kWh")
    print(f"   Net CAPEX: ${sol1['net_capex']/1e6:.2f}M")
    print(f"   CAPEX Reduction: -{sol1['capex_reduction_pct']:.0f}%")
    print(f"   IRR: {sol1['irr']*100:.1f}%")
    print(f"   Payback: {sol1['payback_years']:.1f} years")
    
    # Battery optimization
    sol2 = results['battery_optimization']
    print("\n2. Battery Optimization:")
    if 'battery_kw' in sol2:
        print(f"   Battery Power: {sol2['battery_kw']:.0f} kW")
        print(f"   Battery Energy: {sol2['battery_kwh']:.0f} kWh")
        print(f"   Duration: {sol2['duration_hours']:.1f} hours")
        print(f"   Battery Cost: ${sol2['battery_cost']/1e6:.2f}M")
        print(f"   IRR: {sol2['irr']*100:.1f}%")
    
    # Revenue streams optimization
    sol3 = results['revenue_optimization']
    print("\n3. Revenue Streams Optimization:")
    print(f"   Base PPA Revenue: ${sol3['base_revenue']/1e3:.0f}k")
    if 'platform_fees' in sol3:
        print(f"   Platform Fees: ${sol3['platform_fees']/1e3:.0f}k")
    print(f"   Grid Services: ${sol3['grid_services']/1e3:.0f}k")
    print(f"   EV Charging: ${sol3['ev_charging']/1e3:.0f}k")
    print(f"   REC Sales: ${sol3['rec_sales']/1e3:.0f}k")
    print(f"   Total Revenue: ${sol3['total_revenue']/1e3:.0f}k")
    print(f"   IRR: {sol3['irr']*100:.1f}%")
    
    # Best solution
    best = results['best_solution']
    print("\n" + "="*80)
    print("BEST OVERALL SOLUTION")
    print("="*80)
    print(f"\nStrategy: {best['strategy']}")
    print(f"  PPA Rate: {sol1['ppa_rate']:.2f}¢/kWh (market-competitive)")
    print(f"  Net CAPEX: ${best['net_capex']/1e6:.2f}M")
    print(f"  CAPEX Reduction: -{sol1['capex_reduction_pct']:.0f}%")
    print(f"  Total Revenue: ${sol3['total_revenue']/1e3:.0f}k/year")
    print(f"  Annual OPEX: ${sol1['annual_opex']/1e3:.0f}k/year")
    print(f"  Annual Cash Flow: ${sol1['annual_cash_flow']/1e3:.0f}k/year")
    target_status = 'TARGET MET!' if best['irr'] >= 0.10 else 'Below Target'
    print(f"\n  IRR: {best['irr']*100:.1f}% [{target_status}]")
    print(f"  Payback: {best['payback_years']:.1f} years")
    print(f"  NPV: ${best['npv']/1e6:.2f}M")
    
    print("\n" + "="*80)
    print("CREATING VISUALIZATION...")
    print("="*80)
    
    # Create comprehensive visualization
    plot_optimization_results(results, 
                             save_path='visualizations/irr_optimization_results.png')
    
    print("\n" + "="*80)
    print("OPTIMIZATION COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  [CHART] visualizations/irr_optimization_results.png")
    print("\nThis visualization shows:")
    print("  - Optimization results comparison")
    print("  - Best solution details")
    print("  - Optimal battery configuration")
    print("  - Revenue streams breakdown")
    print("  - Parameter sensitivity")
    print("  - CAPEX reduction breakdown")
    print("  - Optimization path")
    print("  - Implementation roadmap")

