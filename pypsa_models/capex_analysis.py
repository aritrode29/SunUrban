"""
CAPEX Analysis for Urban DER Exchange
======================================

Calculates capital expenditures, financial metrics, and payback analysis
for solar canopy installations with battery storage.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# Cost assumptions (based on NREL ATB and industry standards)
COST_ASSUMPTIONS = {
    'solar_pv': {
        'cost_per_kw': 1200,  # $/kW for commercial canopy systems
        'description': 'Solar PV panels + mounting structure'
    },
    'battery_storage': {
        'cost_per_kw': 800,   # $/kW power capacity
        'cost_per_kwh': 400,  # $/kWh energy capacity
        'description': 'Lithium-ion battery system'
    },
    'inverter': {
        'cost_per_kw': 150,   # $/kW for inverters
        'description': 'DC/AC inverters'
    },
    'electrical': {
        'cost_per_kw': 200,   # $/kW for electrical infrastructure
        'description': 'Wiring, transformers, switchgear'
    },
    'installation': {
        'cost_per_kw': 250,   # $/kW for installation labor
        'description': 'Installation and commissioning'
    },
    'engineering': {
        'cost_per_kw': 100,   # $/kW for engineering/design
        'description': 'Engineering, design, permits'
    },
    'contingency': {
        'percentage': 0.10,   # 10% contingency
        'description': 'Project contingency'
    },
    'itc_rate': {
        'rate': 0.0,          # 0% - ITC removed (going down/expiring)
        'description': 'No ITC credit applied'
    },
    'opex_per_kw': {
        'annual': 25,          # $/kW/year for O&M
        'description': 'Operations & maintenance'
    }
}


def calculate_site_capex(solar_capacity_kw, battery_power_kw, battery_energy_kwh):
    """
    Calculate total CAPEX for a single site.
    
    Parameters:
    -----------
    solar_capacity_kw : float
        Solar PV capacity in kW
    battery_power_kw : float
        Battery power capacity in kW
    battery_energy_kwh : float
        Battery energy capacity in kWh
    
    Returns:
    --------
    dict
        Detailed CAPEX breakdown
    """
    costs = {}
    
    # Solar PV
    costs['solar_pv'] = solar_capacity_kw * COST_ASSUMPTIONS['solar_pv']['cost_per_kw']
    
    # Battery storage
    costs['battery_power'] = battery_power_kw * COST_ASSUMPTIONS['battery_storage']['cost_per_kw']
    costs['battery_energy'] = battery_energy_kwh * COST_ASSUMPTIONS['battery_storage']['cost_per_kwh']
    costs['battery_total'] = costs['battery_power'] + costs['battery_energy']
    
    # Inverter (for solar + battery)
    total_inverter_capacity = solar_capacity_kw + battery_power_kw
    costs['inverter'] = total_inverter_capacity * COST_ASSUMPTIONS['inverter']['cost_per_kw']
    
    # Electrical infrastructure
    costs['electrical'] = solar_capacity_kw * COST_ASSUMPTIONS['electrical']['cost_per_kw']
    
    # Installation
    costs['installation'] = solar_capacity_kw * COST_ASSUMPTIONS['installation']['cost_per_kw']
    
    # Engineering
    costs['engineering'] = solar_capacity_kw * COST_ASSUMPTIONS['engineering']['cost_per_kw']
    
    # Subtotal (before contingency)
    costs['subtotal'] = (costs['solar_pv'] + costs['battery_total'] + 
                        costs['inverter'] + costs['electrical'] + 
                        costs['installation'] + costs['engineering'])
    
    # Contingency
    costs['contingency'] = costs['subtotal'] * COST_ASSUMPTIONS['contingency']['percentage']
    
    # Total CAPEX (before ITC)
    costs['total_capex'] = costs['subtotal'] + costs['contingency']
    
    # ITC credit
    costs['itc_credit'] = costs['total_capex'] * COST_ASSUMPTIONS['itc_rate']['rate']
    
    # Net CAPEX (after ITC)
    costs['net_capex'] = costs['total_capex'] - costs['itc_credit']
    
    # Cost per kW
    costs['cost_per_kw'] = costs['total_capex'] / solar_capacity_kw
    
    # Annual OPEX
    costs['annual_opex'] = solar_capacity_kw * COST_ASSUMPTIONS['opex_per_kw']['annual']
    
    return costs


def calculate_financial_metrics(annual_revenue, annual_opex, net_capex, 
                                project_lifetime=25, discount_rate=0.08):
    """
    Calculate financial metrics: NPV, IRR, payback period.
    
    Parameters:
    -----------
    annual_revenue : float
        Annual revenue in USD
    annual_opex : float
        Annual operating expenses in USD
    net_capex : float
        Net capital expenditure (after ITC) in USD
    project_lifetime : int
        Project lifetime in years (default: 25)
    discount_rate : float
        Discount rate for NPV (default: 8%)
    
    Returns:
    --------
    dict
        Financial metrics
    """
    metrics = {}
    
    # Annual cash flow
    annual_cash_flow = annual_revenue - annual_opex
    metrics['annual_cash_flow'] = annual_cash_flow
    
    # Payback period (simple)
    if annual_cash_flow > 0:
        metrics['payback_years'] = net_capex / annual_cash_flow
    else:
        metrics['payback_years'] = float('inf')
    
    # NPV calculation
    npv = -net_capex
    for year in range(1, project_lifetime + 1):
        npv += annual_cash_flow / ((1 + discount_rate) ** year)
    metrics['npv'] = npv
    
    # IRR calculation (simplified - find rate where NPV = 0)
    # Using binary search approximation
    irr_low = 0.0
    irr_high = 0.5
    tolerance = 0.001
    
    for _ in range(100):  # Max iterations
        irr_test = (irr_low + irr_high) / 2
        npv_test = -net_capex
        for year in range(1, project_lifetime + 1):
            npv_test += annual_cash_flow / ((1 + irr_test) ** year)
        
        if abs(npv_test) < tolerance:
            break
        elif npv_test > 0:
            irr_low = irr_test
        else:
            irr_high = irr_test
    
    metrics['irr'] = irr_test if annual_cash_flow > 0 else 0.0
    
    # ROI (simple)
    total_revenue = annual_revenue * project_lifetime
    total_opex = annual_opex * project_lifetime
    total_profit = total_revenue - total_opex - net_capex
    metrics['roi'] = (total_profit / net_capex) * 100 if net_capex > 0 else 0.0
    
    # LCOE (Levelized Cost of Energy) - simplified
    # Would need annual generation for accurate LCOE
    metrics['lcoe_note'] = 'LCOE requires annual generation data'
    
    return metrics


def analyze_all_sites_capex(site_capacities, annual_revenues):
    """
    Analyze CAPEX for all sites and calculate aggregate metrics.
    
    Parameters:
    -----------
    site_capacities : dict
        {'Site_A': {'solar_kw': 550, 'battery_kw': 550, 'battery_kwh': 1100}, ...}
    annual_revenues : dict
        {'S1': 290000, 'S2': 263000, ...}  # Annual revenue per scenario
    
    Returns:
    --------
    dict
        Complete CAPEX analysis for all sites
    """
    analysis = {
        'sites': {},
        'aggregate': {},
        'scenarios': {}
    }
    
    # Calculate CAPEX for each site
    total_solar_kw = 0
    total_battery_kw = 0
    total_battery_kwh = 0
    total_capex = 0
    total_net_capex = 0
    total_opex = 0
    
    for site_name, capacities in site_capacities.items():
        site_capex = calculate_site_capex(
            capacities['solar_kw'],
            capacities['battery_kw'],
            capacities['battery_kwh']
        )
        analysis['sites'][site_name] = site_capex
        
        total_solar_kw += capacities['solar_kw']
        total_battery_kw += capacities['battery_kw']
        total_battery_kwh += capacities['battery_kwh']
        total_capex += site_capex['total_capex']
        total_net_capex += site_capex['net_capex']
        total_opex += site_capex['annual_opex']
    
    # Aggregate metrics
    analysis['aggregate'] = {
        'total_solar_kw': total_solar_kw,
        'total_battery_kw': total_battery_kw,
        'total_battery_kwh': total_battery_kwh,
        'total_capex': total_capex,
        'total_net_capex': total_net_capex,
        'total_opex': total_opex,
        'cost_per_kw': total_capex / total_solar_kw if total_solar_kw > 0 else 0,
        'cost_per_mw': (total_capex / total_solar_kw) * 1000 if total_solar_kw > 0 else 0
    }
    
    # Financial metrics for each scenario
    for scenario, revenue in annual_revenues.items():
        metrics = calculate_financial_metrics(
            revenue,
            total_opex,
            total_net_capex
        )
        analysis['scenarios'][scenario] = {
            'annual_revenue': revenue,
            'annual_opex': total_opex,
            'net_capex': total_net_capex,
            **metrics
        }
    
    return analysis


def plot_capex_breakdown(capex_analysis, save_path='visualizations/capex_breakdown.png'):
    """
    Create comprehensive CAPEX visualization.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    sites = capex_analysis['sites']
    aggregate = capex_analysis['aggregate']
    scenarios = capex_analysis['scenarios']
    
    # 1. CAPEX breakdown by component (pie chart)
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Aggregate costs by component
    component_costs = {
        'Solar PV': sum([s['solar_pv'] for s in sites.values()]),
        'Battery': sum([s['battery_total'] for s in sites.values()]),
        'Inverter': sum([s['inverter'] for s in sites.values()]),
        'Electrical': sum([s['electrical'] for s in sites.values()]),
        'Installation': sum([s['installation'] for s in sites.values()]),
        'Engineering': sum([s['engineering'] for s in sites.values()]),
        'Contingency': sum([s['contingency'] for s in sites.values()])
    }
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
    wedges, texts, autotexts = ax1.pie(
        component_costs.values(),
        labels=component_costs.keys(),
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    ax1.set_title('CAPEX Breakdown by Component\n(3 Sites Total)', 
                 fontsize=12, fontweight='bold')
    
    # 2. CAPEX by site (bar chart)
    ax2 = fig.add_subplot(gs[0, 1])
    
    site_names = list(sites.keys())
    site_capex = [sites[s]['total_capex'] / 1e6 for s in site_names]  # Convert to millions
    site_net_capex = [sites[s]['net_capex'] / 1e6 for s in site_names]
    
    x_pos = np.arange(len(site_names))
    width = 0.35
    
    bars1 = ax2.bar(x_pos - width/2, site_capex, width, label='Total CAPEX', 
                   color='#FF6B6B', alpha=0.8, edgecolor='black')
    bars2 = ax2.bar(x_pos + width/2, site_net_capex, width, label='Net CAPEX (No ITC)', 
                   color='#4ECDC4', alpha=0.8, edgecolor='black')
    
    ax2.set_xlabel('Site', fontsize=11, fontweight='bold')
    ax2.set_ylabel('CAPEX ($M)', fontsize=11, fontweight='bold')
    ax2.set_title('CAPEX by Site', fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(site_names)
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}M', ha='center', va='bottom', fontsize=9)
    
    # 3. Financial metrics comparison
    ax3 = fig.add_subplot(gs[0, 2])
    
    scenario_names = list(scenarios.keys())
    payback_years = [scenarios[s]['payback_years'] for s in scenario_names]
    irr_values = [scenarios[s]['irr'] * 100 for s in scenario_names]  # Convert to percentage
    
    x_pos = np.arange(len(scenario_names))
    ax3_twin = ax3.twinx()
    
    bars1 = ax3.bar(x_pos - width/2, payback_years, width, label='Payback (years)', 
                   color='#FF6B6B', alpha=0.8, edgecolor='black')
    line1 = ax3_twin.plot(x_pos, irr_values, 'o-', color='#4ECDC4', 
                          linewidth=3, markersize=10, label='IRR (%)')
    
    ax3.set_xlabel('Scenario', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Payback Period (years)', fontsize=11, fontweight='bold', color='#FF6B6B')
    ax3_twin.set_ylabel('IRR (%)', fontsize=11, fontweight='bold', color='#4ECDC4')
    ax3.set_title('Financial Metrics by Scenario', fontsize=12, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(scenario_names)
    ax3.tick_params(axis='y', labelcolor='#FF6B6B')
    ax3_twin.tick_params(axis='y', labelcolor='#4ECDC4')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        if height < 50:  # Don't label if payback > 50 years
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}y', ha='center', va='bottom', fontsize=9)
    
    for i, irr in enumerate(irr_values):
        ax3_twin.text(i, irr, f'{irr:.1f}%', ha='center', va='bottom', 
                     fontsize=9, color='#4ECDC4', fontweight='bold')
    
    # Combine legends
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)
    
    # 4. NPV by scenario
    ax4 = fig.add_subplot(gs[1, 0])
    
    npv_values = [scenarios[s]['npv'] / 1e6 for s in scenario_names]  # Convert to millions
    colors_npv = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in npv_values]
    
    bars = ax4.bar(scenario_names, npv_values, color=colors_npv, alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    ax4.axhline(y=0, color='k', linestyle='--', linewidth=2)
    ax4.set_xlabel('Scenario', fontsize=11, fontweight='bold')
    ax4.set_ylabel('NPV ($M)', fontsize=11, fontweight='bold')
    ax4.set_title('Net Present Value (25 years, 8% discount)', 
                 fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, npv_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'${val:.2f}M', ha='center', 
                va='bottom' if val > 0 else 'top', fontsize=10, fontweight='bold')
    
    # 5. Cost per kW comparison
    ax5 = fig.add_subplot(gs[1, 1])
    
    cost_per_kw = [sites[s]['cost_per_kw'] for s in site_names]
    industry_benchmark = 1400  # $/kW industry average
    
    bars = ax5.bar(site_names, cost_per_kw, color='#45B7D1', alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    ax5.axhline(y=industry_benchmark, color='r', linestyle='--', 
               linewidth=2, label=f'Industry Avg: ${industry_benchmark}/kW')
    ax5.set_xlabel('Site', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Cost per kW ($)', fontsize=11, fontweight='bold')
    ax5.set_title('Cost per kW by Site', fontsize=12, fontweight='bold')
    ax5.legend(framealpha=0.9)
    ax5.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, cost_per_kw):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'${val:.0f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    # 6. Cash flow projection (first scenario)
    ax6 = fig.add_subplot(gs[1, 2])
    
    if scenarios:
        first_scenario = list(scenarios.keys())[0]
        scenario_data = scenarios[first_scenario]
        
        years = np.arange(0, 26)  # 0-25 years
        cash_flows = np.zeros(26)
        cash_flows[0] = -scenario_data['net_capex']  # Initial investment
        for year in range(1, 26):
            cash_flows[year] = scenario_data['annual_cash_flow']
        
        cumulative_cf = np.cumsum(cash_flows)
        
        ax6.plot(years, cumulative_cf / 1e6, 'o-', linewidth=3, markersize=6, 
                color='#4ECDC4', label='Cumulative Cash Flow')
        ax6.axhline(y=0, color='k', linestyle='--', linewidth=2)
        ax6.fill_between(years, 0, cumulative_cf / 1e6, 
                        where=(cumulative_cf >= 0), alpha=0.3, color='green')
        ax6.fill_between(years, 0, cumulative_cf / 1e6, 
                        where=(cumulative_cf < 0), alpha=0.3, color='red')
        
        # Mark payback point
        payback = scenario_data['payback_years']
        if payback < 25:
            ax6.axvline(x=payback, color='r', linestyle=':', linewidth=2, 
                       label=f'Payback: {payback:.1f} years')
        
        ax6.set_xlabel('Year', fontsize=11, fontweight='bold')
        ax6.set_ylabel('Cumulative Cash Flow ($M)', fontsize=11, fontweight='bold')
        ax6.set_title(f'Cash Flow Projection\n({first_scenario})', 
                     fontsize=12, fontweight='bold')
        ax6.legend(framealpha=0.9)
        ax6.grid(True, alpha=0.3)
    
    # 7. Revenue vs CAPEX comparison
    ax7 = fig.add_subplot(gs[2, :2])
    
    scenario_names_list = list(scenarios.keys())
    annual_revenues_list = [scenarios[s]['annual_revenue'] / 1e6 for s in scenario_names_list]
    net_capex_list = [scenarios[s]['net_capex'] / 1e6 for s in scenario_names_list]
    
    x_pos = np.arange(len(scenario_names_list))
    width = 0.35
    
    bars1 = ax7.bar(x_pos - width/2, net_capex_list, width, label='Net CAPEX', 
                   color='#FF6B6B', alpha=0.8, edgecolor='black')
    bars2 = ax7.bar(x_pos + width/2, annual_revenues_list, width, label='Annual Revenue', 
                   color='#4ECDC4', alpha=0.8, edgecolor='black')
    
    ax7.set_xlabel('Scenario', fontsize=11, fontweight='bold')
    ax7.set_ylabel('Amount ($M)', fontsize=11, fontweight='bold')
    ax7.set_title('CAPEX vs Annual Revenue', fontsize=12, fontweight='bold')
    ax7.set_xticks(x_pos)
    ax7.set_xticklabels(scenario_names_list)
    ax7.legend(framealpha=0.9)
    ax7.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax7.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}M', ha='center', va='bottom', fontsize=9)
    
    # 8. Summary table
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.axis('off')
    
    summary_text = f"""
    FINANCIAL SUMMARY
    {'='*40}
    
    Total System Size:
        {aggregate['total_solar_kw']:.0f} kW Solar
        {aggregate['total_battery_kw']:.0f} kW / {aggregate['total_battery_kwh']:.0f} kWh Battery
    
    Total CAPEX:
        ${aggregate['total_capex']/1e6:.2f}M (Total CAPEX)
        ${aggregate['total_net_capex']/1e6:.2f}M (Net CAPEX, No ITC)
    
    Cost per kW:
        ${aggregate['cost_per_kw']:.0f}/kW
        ${aggregate['cost_per_mw']:.0f}/MW
    
    Annual OPEX:
        ${aggregate['total_opex']/1e3:.0f}k/year
    
    Best Scenario:
        {max(scenarios.items(), key=lambda x: x[1]['irr'])[0]}
        IRR: {max([s['irr']*100 for s in scenarios.values()]):.1f}%
        Payback: {min([s['payback_years'] for s in scenarios.values()]):.1f} years
    """
    
    ax8.text(0.1, 0.9, summary_text, transform=ax8.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    plt.suptitle('CAPEX Analysis - Urban DER Exchange\n' + 
                'Solar Canopy + Battery Storage (3 Sites)',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"CAPEX analysis saved to: {save_path}")
    
    return fig


if __name__ == "__main__":
    # Example usage
    site_capacities = {
        'Site_A': {'solar_kw': 550, 'battery_kw': 550, 'battery_kwh': 1100},
        'Site_B': {'solar_kw': 380, 'battery_kw': 380, 'battery_kwh': 760},
        'Site_C': {'solar_kw': 800, 'battery_kw': 800, 'battery_kwh': 1600}
    }
    
    annual_revenues = {
        'S1': 290000,  # BTM PPA
        'S2': 263000,  # Hybrid
        'S3': 263000,  # VPP
        'S4': 193000   # Marketplace
    }
    
    analysis = analyze_all_sites_capex(site_capacities, annual_revenues)
    
    print("\n" + "="*80)
    print("CAPEX ANALYSIS RESULTS")
    print("="*80)
    print(f"\nTotal CAPEX (3 sites): ${analysis['aggregate']['total_capex']/1e6:.2f}M")
    print(f"Net CAPEX (after ITC): ${analysis['aggregate']['total_net_capex']/1e6:.2f}M")
    print(f"Cost per kW: ${analysis['aggregate']['cost_per_kw']:.0f}/kW")
    print(f"Cost per MW: ${analysis['aggregate']['cost_per_mw']:.0f}/MW")
    
    print("\nFinancial Metrics by Scenario:")
    for scenario, data in analysis['scenarios'].items():
        print(f"\n{scenario}:")
        print(f"  Annual Revenue: ${data['annual_revenue']/1e3:.0f}k")
        print(f"  Payback: {data['payback_years']:.1f} years")
        print(f"  IRR: {data['irr']*100:.1f}%")
        print(f"  NPV: ${data['npv']/1e6:.2f}M")
    
    # Create visualization
    plot_capex_breakdown(analysis)

