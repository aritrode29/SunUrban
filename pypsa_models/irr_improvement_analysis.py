"""
IRR Improvement Analysis
========================

Analyzes how to improve IRR through revenue increases, cost reductions, and optimization.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from capex_analysis import calculate_financial_metrics, COST_ASSUMPTIONS


def analyze_irr_improvements(base_annual_revenue, base_net_capex, base_annual_opex,
                             project_lifetime=25, discount_rate=0.08):
    """
    Analyze how different improvements affect IRR.
    
    Parameters:
    -----------
    base_annual_revenue : float
        Current annual revenue
    base_net_capex : float
        Current net CAPEX (after ITC)
    base_annual_opex : float
        Current annual OPEX
    project_lifetime : int
        Project lifetime
    discount_rate : float
        Discount rate for NPV
    
    Returns:
    --------
    dict
        Analysis of improvement scenarios
    """
    improvements = {}
    
    # Current baseline
    baseline = calculate_financial_metrics(
        base_annual_revenue, base_annual_opex, base_net_capex,
        project_lifetime, discount_rate
    )
    improvements['Baseline'] = baseline
    
    # Scenario 1: Increase revenue by 20%
    revenue_20pct = base_annual_revenue * 1.20
    metrics_1 = calculate_financial_metrics(
        revenue_20pct, base_annual_opex, base_net_capex,
        project_lifetime, discount_rate
    )
    improvements['+20% Revenue'] = metrics_1
    
    # Scenario 2: Increase revenue by 50%
    revenue_50pct = base_annual_revenue * 1.50
    metrics_2 = calculate_financial_metrics(
        revenue_50pct, base_annual_opex, base_net_capex,
        project_lifetime, discount_rate
    )
    improvements['+50% Revenue'] = metrics_2
    
    # Scenario 3: Reduce CAPEX by 20%
    capex_reduced = base_net_capex * 0.80
    metrics_3 = calculate_financial_metrics(
        base_annual_revenue, base_annual_opex, capex_reduced,
        project_lifetime, discount_rate
    )
    improvements['-20% CAPEX'] = metrics_3
    
    # Scenario 4: Reduce CAPEX by 30%
    capex_reduced_30 = base_net_capex * 0.70
    metrics_4 = calculate_financial_metrics(
        base_annual_revenue, base_annual_opex, capex_reduced_30,
        project_lifetime, discount_rate
    )
    improvements['-30% CAPEX'] = metrics_4
    
    # Scenario 5: Reduce battery costs (batteries are 40% of CAPEX)
    # Assume battery costs drop 50% (from $400/kWh to $200/kWh)
    battery_savings = base_net_capex * 0.40 * 0.50  # 40% of CAPEX, 50% reduction
    capex_battery_reduction = base_net_capex - battery_savings
    metrics_5 = calculate_financial_metrics(
        base_annual_revenue, base_annual_opex, capex_battery_reduction,
        project_lifetime, discount_rate
    )
    improvements['Battery Cost -50%'] = metrics_5
    
    # Scenario 6: Combined - Revenue +20% and CAPEX -20%
    metrics_6 = calculate_financial_metrics(
        revenue_20pct, base_annual_opex, capex_reduced,
        project_lifetime, discount_rate
    )
    improvements['+20% Rev & -20% CAPEX'] = metrics_6
    
    # Scenario 7: Higher PPA rate (from 9¢ to 12¢/kWh)
    # Assuming 8.82 MWh/day generation, 365 days = 3,219 MWh/year
    # At 9¢/kWh = $290k, at 12¢/kWh = $386k
    revenue_higher_ppa = base_annual_revenue * (12.0 / 9.0)
    metrics_7 = calculate_financial_metrics(
        revenue_higher_ppa, base_annual_opex, base_net_capex,
        project_lifetime, discount_rate
    )
    improvements['PPA 12¢/kWh'] = metrics_7
    
    # Scenario 8: Add grid services revenue (+$50k/year)
    revenue_grid_services = base_annual_revenue + 50000
    metrics_8 = calculate_financial_metrics(
        revenue_grid_services, base_annual_opex, base_net_capex,
        project_lifetime, discount_rate
    )
    improvements['+Grid Services'] = metrics_8
    
    # Scenario 9: Optimize battery sizing (reduce from 2h to 1h)
    # Battery is 40% of CAPEX, reducing duration by 50% saves ~20% of battery cost
    battery_optimization_savings = base_net_capex * 0.40 * 0.20
    capex_optimized = base_net_capex - battery_optimization_savings
    metrics_9 = calculate_financial_metrics(
        base_annual_revenue, base_annual_opex, capex_optimized,
        project_lifetime, discount_rate
    )
    improvements['Optimize Battery'] = metrics_9
    
    # Scenario 10: Best case - Higher revenue + lower CAPEX
    metrics_10 = calculate_financial_metrics(
        revenue_50pct, base_annual_opex, capex_reduced_30,
        project_lifetime, discount_rate
    )
    improvements['Best Case'] = metrics_10
    
    return improvements


def plot_irr_improvements(improvements, base_net_capex=None, base_annual_opex=None,
                         save_path='visualizations/irr_improvement_analysis.png'):
    """
    Create visualization of IRR improvement scenarios.
    
    Parameters:
    -----------
    improvements : dict
        Dictionary of improvement scenarios with financial metrics
    base_net_capex : float, optional
        Base net CAPEX (if not provided, will estimate from baseline)
    base_annual_opex : float, optional
        Base annual OPEX (if not provided, will estimate from baseline)
    save_path : str
        Path to save visualization
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    scenario_names = list(improvements.keys())
    irr_values = [imp['irr'] * 100 for imp in improvements.values()]
    payback_values = [imp['payback_years'] for imp in improvements.values()]
    npv_values = [imp['npv'] / 1e6 for imp in improvements.values()]
    annual_cf = [imp['annual_cash_flow'] / 1e3 for imp in improvements.values()]
    
    # Estimate base values if not provided
    if base_net_capex is None:
        # Estimate from baseline scenario
        baseline = improvements['Baseline']
        # Reverse engineer: payback = capex / cash_flow
        base_net_capex = baseline['payback_years'] * baseline['annual_cash_flow']
    
    if base_annual_opex is None:
        # Estimate from baseline
        baseline = improvements['Baseline']
        # Annual revenue = cash flow + opex, estimate opex as 15% of revenue
        estimated_revenue = baseline['annual_cash_flow'] * 1.15
        base_annual_opex = estimated_revenue - baseline['annual_cash_flow']
    
    # 1. IRR comparison
    ax1 = fig.add_subplot(gs[0, 0])
    
    colors = ['#FF6B6B' if irr < 5 else '#4ECDC4' if irr < 10 else '#45B7D1' 
              for irr in irr_values]
    
    bars = ax1.barh(scenario_names, irr_values, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax1.axvline(x=5, color='orange', linestyle='--', linewidth=2, label='5% Target')
    ax1.axvline(x=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax1.set_xlabel('IRR (%)', fontsize=11, fontweight='bold')
    ax1.set_title('IRR by Improvement Scenario', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, alpha=0.3, axis='x')
    
    for bar, val in zip(bars, irr_values):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', ha='left' if width > 0 else 'right', 
                va='center', fontsize=9, fontweight='bold')
    
    # 2. Payback period
    ax2 = fig.add_subplot(gs[0, 1])
    
    colors_pb = ['#FF6B6B' if pb > 15 else '#4ECDC4' if pb > 10 else '#45B7D1' 
                 for pb in payback_values]
    
    bars = ax2.barh(scenario_names, payback_values, color=colors_pb, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax2.axvline(x=10, color='green', linestyle='--', linewidth=2, label='10yr Target')
    ax2.set_xlabel('Payback Period (years)', fontsize=11, fontweight='bold')
    ax2.set_title('Payback Period by Scenario', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.3, axis='x')
    
    for bar, val in zip(bars, payback_values):
        if val < 50:  # Don't label if > 50 years
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'{val:.1f}y', ha='left', va='center', 
                    fontsize=9, fontweight='bold')
    
    # 3. NPV comparison
    ax3 = fig.add_subplot(gs[0, 2])
    
    colors_npv = ['#FF6B6B' if npv < 0 else '#4ECDC4' for npv in npv_values]
    
    bars = ax3.barh(scenario_names, npv_values, color=colors_npv, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax3.axvline(x=0, color='k', linestyle='-', linewidth=2)
    ax3.set_xlabel('NPV ($M)', fontsize=11, fontweight='bold')
    ax3.set_title('Net Present Value (25yr, 8%)', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='x')
    
    for bar, val in zip(bars, npv_values):
        width = bar.get_width()
        ax3.text(width, bar.get_y() + bar.get_height()/2,
                f'${val:.2f}M', ha='left' if val > 0 else 'right',
                va='center', fontsize=9, fontweight='bold')
    
    # 4. Sensitivity: Revenue impact
    ax4 = fig.add_subplot(gs[1, 0])
    
    revenue_multipliers = np.arange(0.8, 2.1, 0.1)
    baseline = improvements['Baseline']
    # Estimate base revenue from cash flow
    base_revenue = baseline['annual_cash_flow'] + base_annual_opex
    base_capex = base_net_capex
    
    # Calculate IRR for different revenue levels
    irr_sensitivity = []
    for mult in revenue_multipliers:
        test_revenue = base_revenue * mult
        test_opex = base_annual_opex
        # Approximate: need to recalculate, but for now use simplified
        test_metrics = calculate_financial_metrics(
            test_revenue, test_opex, base_net_capex, 25, 0.08
        )
        irr_sensitivity.append(test_metrics['irr'] * 100)
    
    ax4.plot(revenue_multipliers * 100, irr_sensitivity, 'o-', 
            linewidth=3, markersize=8, color='#4ECDC4')
    ax4.axhline(y=5, color='orange', linestyle='--', linewidth=2, label='5% Target')
    ax4.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax4.axvline(x=100, color='k', linestyle=':', linewidth=1, alpha=0.5, label='Baseline')
    ax4.set_xlabel('Revenue (% of Baseline)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('IRR (%)', fontsize=11, fontweight='bold')
    ax4.set_title('IRR Sensitivity to Revenue', fontsize=12, fontweight='bold')
    ax4.legend(framealpha=0.9)
    ax4.grid(True, alpha=0.3)
    
    # 5. Sensitivity: CAPEX impact
    ax5 = fig.add_subplot(gs[1, 1])
    
    capex_multipliers = np.arange(0.5, 1.1, 0.05)
    base_revenue_for_capex = baseline['annual_cash_flow'] + base_annual_opex
    
    irr_capex_sensitivity = []
    for mult in capex_multipliers:
        test_capex = base_capex * mult
        test_metrics = calculate_financial_metrics(
            base_revenue_for_capex, base_annual_opex, 
            test_capex, 25, 0.08
        )
        irr_capex_sensitivity.append(test_metrics['irr'] * 100)
    
    ax5.plot(capex_multipliers * 100, irr_capex_sensitivity, 's-',
            linewidth=3, markersize=8, color='#FF6B6B')
    ax5.axhline(y=5, color='orange', linestyle='--', linewidth=2, label='5% Target')
    ax5.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax5.axvline(x=100, color='k', linestyle=':', linewidth=1, alpha=0.5, label='Baseline')
    ax5.set_xlabel('CAPEX (% of Baseline)', fontsize=11, fontweight='bold')
    ax5.set_ylabel('IRR (%)', fontsize=11, fontweight='bold')
    ax5.set_title('IRR Sensitivity to CAPEX', fontsize=12, fontweight='bold')
    ax5.legend(framealpha=0.9)
    ax5.grid(True, alpha=0.3)
    
    # 6. Improvement recommendations
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    # Find scenarios that meet targets
    target_irr = 10.0
    viable_scenarios = [name for name, imp in improvements.items() 
                       if imp['irr'] * 100 >= target_irr]
    
    if viable_scenarios:
        best = max(viable_scenarios, key=lambda x: improvements[x]['irr'])
        best_irr = improvements[best]['irr'] * 100
        best_payback = improvements[best]['payback_years']
    else:
        best = max(improvements.items(), key=lambda x: x[1]['irr'])[0]
        best_irr = improvements[best]['irr'] * 100
        best_payback = improvements[best]['payback_years']
    
    recommendations = f"""
    IMPROVEMENT RECOMMENDATIONS
    {'='*40}
    
    Current Baseline:
        IRR: {improvements['Baseline']['irr']*100:.1f}%
        Payback: {improvements['Baseline']['payback_years']:.1f} years
        NPV: ${improvements['Baseline']['npv']/1e6:.2f}M
    
    Best Scenario: {best}
        IRR: {best_irr:.1f}%
        Payback: {best_payback:.1f} years
    
    Top Improvements:
    1. Increase Revenue
       - Higher PPA rates (9¢ → 12¢)
       - Add grid services
       - Scale to more sites
    
    2. Reduce CAPEX
       - Battery cost reduction
       - Optimize battery sizing
       - Scale economies
    
    3. Combined Approach
       - Revenue +20% & CAPEX -20%
       - Can achieve 5-10% IRR
    
    Target Metrics:
        IRR: 10-15%
        Payback: 6-10 years
        NPV: Positive
    """
    
    ax6.text(0.1, 0.9, recommendations, transform=ax6.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8))
    
    # 7. Revenue vs CAPEX trade-off
    ax7 = fig.add_subplot(gs[2, :2])
    
    # Create contour of IRR levels
    revenue_range = np.linspace(base_revenue_for_capex * 0.7, base_revenue_for_capex * 2.0, 20)
    capex_range = np.linspace(base_net_capex * 0.5, base_net_capex * 1.0, 20)
    
    R, C = np.meshgrid(revenue_range, capex_range)
    IRR_grid = np.zeros_like(R)
    
    for i in range(len(capex_range)):
        for j in range(len(revenue_range)):
            test_metrics = calculate_financial_metrics(
                revenue_range[j], base_annual_opex,
                capex_range[i], 25, 0.08
            )
            IRR_grid[i, j] = test_metrics['irr'] * 100
    
    contour = ax7.contourf(R / 1e6, C / 1e6, IRR_grid, levels=[0, 5, 10, 15, 20, 25],
                           colors=['#FF6B6B', '#FFA07A', '#FFD700', '#98D8C8', '#4ECDC4'],
                           alpha=0.6)
    ax7.contour(R / 1e6, C / 1e6, IRR_grid, levels=[5, 10, 15], 
               colors='black', linewidths=2, linestyles='--')
    
    # Mark baseline
    ax7.plot(base_revenue_for_capex / 1e6, base_net_capex / 1e6, 'ro', 
            markersize=15, label='Baseline', zorder=10)
    
    # Mark improvement scenarios
    for name, imp in improvements.items():
        if name != 'Baseline':
            # Estimate revenue and capex for this scenario
            if '+20% Revenue' in name:
                rev = base_revenue_for_capex * 1.2
                cap = base_capex
            elif '+50% Revenue' in name:
                rev = base_revenue_for_capex * 1.5
                cap = base_capex
            elif '-20% CAPEX' in name:
                rev = base_revenue_for_capex
                cap = base_capex * 0.8
            elif '-30% CAPEX' in name:
                rev = base_revenue_for_capex
                cap = base_capex * 0.7
            elif 'Best Case' in name:
                rev = base_revenue_for_capex * 1.5
                cap = base_net_capex * 0.7
            else:
                continue
            
            ax7.plot(rev / 1e6, cap / 1e6, 'o', markersize=10, 
                    label=name, zorder=10)
    
    ax7.set_xlabel('Annual Revenue ($M)', fontsize=11, fontweight='bold')
    ax7.set_ylabel('Net CAPEX ($M)', fontsize=11, fontweight='bold')
    ax7.set_title('IRR Contour: Revenue vs CAPEX Trade-off', 
                 fontsize=12, fontweight='bold')
    ax7.legend(loc='upper left', framealpha=0.9, fontsize=8)
    cbar = plt.colorbar(contour, ax=ax7)
    cbar.set_label('IRR (%)', fontsize=10, fontweight='bold')
    
    # 8. Summary table
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.axis('off')
    
    # Create summary table
    table_data = []
    for name, imp in list(improvements.items())[:6]:  # Top 6 scenarios
        table_data.append([
            name[:20],
            f"{imp['irr']*100:.1f}%",
            f"{imp['payback_years']:.1f}y",
            f"${imp['npv']/1e6:.2f}M"
        ])
    
    table = ax8.table(cellText=table_data,
                     colLabels=['Scenario', 'IRR', 'Payback', 'NPV'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor('#4ECDC4')
        table[(0, i)].set_text_props(weight='bold')
    
    plt.suptitle('IRR Improvement Analysis\n' + 
                'How to Achieve 10%+ IRR Targets',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"IRR improvement analysis saved to: {save_path}")
    
    return fig


if __name__ == "__main__":
    # Example: S1 scenario (BTM PPA)
    base_revenue = 290000  # $290k/year
    base_net_capex = 4860000  # $4.86M (after ITC)
    base_opex = 43000  # $43k/year
    
    print("="*80)
    print("IRR IMPROVEMENT ANALYSIS")
    print("="*80)
    
    improvements = analyze_irr_improvements(
        base_revenue, base_net_capex, base_opex
    )
    
    print("\nImprovement Scenarios:")
    print("-" * 80)
    for name, metrics in improvements.items():
        print(f"\n{name}:")
        print(f"  IRR: {metrics['irr']*100:.1f}%")
        print(f"  Payback: {metrics['payback_years']:.1f} years")
        print(f"  NPV: ${metrics['npv']/1e6:.2f}M")
        print(f"  Annual Cash Flow: ${metrics['annual_cash_flow']/1e3:.0f}k")
    
    # Create visualization
    plot_irr_improvements(improvements)

