"""
IRR Improvement Analysis Runner
================================

Analyzes how to improve IRR from current low levels (0-2%) to target levels (10%+).
"""

import sys
sys.path.insert(0, 'pypsa_models')

from irr_improvement_analysis import analyze_irr_improvements, plot_irr_improvements

if __name__ == "__main__":
    print("="*80)
    print("IRR IMPROVEMENT ANALYSIS")
    print("="*80)
    print("\nAnalyzing how to improve IRR from current 0-2% to target 10%+")
    
    # Current baseline (S1: BTM PPA - best scenario)
    base_revenue = 290000      # $290k/year
    base_net_capex = 4860000   # $4.86M (after 30% ITC)
    base_opex = 43000          # $43k/year
    
    print("\nBaseline Scenario (S1: BTM PPA):")
    print(f"  Annual Revenue: ${base_revenue/1e3:.0f}k")
    print(f"  Net CAPEX: ${base_net_capex/1e6:.2f}M")
    print(f"  Annual OPEX: ${base_opex/1e3:.0f}k")
    
    print("\n" + "="*80)
    print("RUNNING IMPROVEMENT ANALYSIS...")
    print("="*80)
    
    improvements = analyze_irr_improvements(
        base_revenue, base_net_capex, base_opex
    )
    
    print("\n" + "="*80)
    print("IMPROVEMENT SCENARIOS")
    print("="*80)
    
    for name, metrics in improvements.items():
        print(f"\n{name}:")
        print(f"  IRR: {metrics['irr']*100:.1f}%")
        print(f"  Payback: {metrics['payback_years']:.1f} years")
        print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
        print(f"  Annual Cash Flow: ${metrics['annual_cash_flow']/1e3:.0f}k")
    
    # Find scenarios meeting 10% IRR target
    target_irr = 10.0
    viable = {name: imp for name, imp in improvements.items() 
              if imp['irr'] * 100 >= target_irr}
    
    print("\n" + "="*80)
    if viable:
        print(f"SCENARIOS MEETING {target_irr}% IRR TARGET:")
        print("="*80)
        for name, metrics in viable.items():
            print(f"\n{name}:")
            print(f"  IRR: {metrics['irr']*100:.1f}%")
            print(f"  Payback: {metrics['payback_years']:.1f} years")
            print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
    else:
        print("NO SCENARIOS MEET 10% IRR TARGET")
        print("="*80)
        print("\nBest achievable scenario:")
        best = max(improvements.items(), key=lambda x: x[1]['irr'])
        print(f"  {best[0]}: {best[1]['irr']*100:.1f}% IRR")
        print(f"\nTo reach 10% IRR, need:")
        print(f"  - Revenue increase: {((target_irr/100 - best[1]['irr']) / best[1]['irr'] + 1) * 100 - 100:.0f}%")
        print(f"  - OR CAPEX reduction: {((best[1]['irr'] / (target_irr/100)) - 1) * 100:.0f}%")
    
    print("\n" + "="*80)
    print("KEY RECOMMENDATIONS")
    print("="*80)
    print("""
1. INCREASE REVENUE:
   - Raise PPA rate from 9c to 12-15c/kWh (+33-67% revenue)
   - Add grid services revenue ($50-100k/year)
   - Scale to 10-20 sites (economies of scale)
   - Add EV charging revenue streams

2. REDUCE CAPEX:
   - Battery costs declining (target: $200/kWh vs current $400/kWh)
   - Optimize battery sizing (1 hour vs 2 hours)
   - Standardize designs (reduce engineering costs)
   - Scale to reduce $/kW

3. COMBINED APPROACH:
   - Revenue +20% AND CAPEX -20% → Can achieve 5-8% IRR
   - Revenue +50% AND CAPEX -30% → Can achieve 10%+ IRR

4. FINANCING OPTIONS:
   - Lower cost of capital (project financing vs equity)
   - Longer payback acceptable for infrastructure
   - Tax equity structures
   - Grants/subsidies
    """)
    
    print("="*80)
    print("CREATING VISUALIZATIONS...")
    print("="*80)
    
    plot_irr_improvements(improvements, 
                         save_path='visualizations/irr_improvement_analysis.png')
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  [CHART] visualizations/irr_improvement_analysis.png")
    print("\nThis visualization shows:")
    print("  - IRR by improvement scenario")
    print("  - Payback period analysis")
    print("  - NPV comparison")
    print("  - Revenue sensitivity")
    print("  - CAPEX sensitivity")
    print("  - Revenue vs CAPEX trade-off map")
    print("  - Improvement recommendations")

