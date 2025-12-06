"""
Plot Optimized PyPSA Outputs
============================

Comprehensive visualization of PyPSA optimization results with optimized parameters.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
import warnings
import sys
sys.path.insert(0, 'pypsa_models')
from optimized_scenario_config import (
    OPTIMIZED_CONFIG, get_optimized_ppa_rate, 
    get_optimized_capex, get_optimized_revenue_streams
)
warnings.filterwarnings('ignore')


def plot_comprehensive_pypsa_outputs(results, save_path='visualizations/optimized_pypsa_comprehensive.png'):
    """
    Create comprehensive visualization of PyPSA optimization outputs.
    """
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(4, 4, figure=fig, hspace=0.4, wspace=0.3)
    
    # Get first scenario for detailed plots
    s1 = results.get('S1')
    if s1 is None:
        print("No S1 results available")
        return None
    
    n = s1['network']
    sites = ['Site_A', 'Site_B', 'Site_C']
    hours = np.arange(24)
    
    # 1. Generation Profiles
    ax1 = fig.add_subplot(gs[0, 0])
    
    for site_name in sites:
        gen_name = f'Canopy_{site_name}'
        if gen_name in n.generators.index:
            gen_kw = n.generators_t.p[gen_name].values * 1000
            ax1.plot(hours, gen_kw, 'o-', label=site_name, linewidth=2, markersize=4)
    
    ax1.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Generation (kW)', fontsize=11, fontweight='bold')
    ax1.set_title('Solar Generation Profiles (Optimized)', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 23)
    
    # 2. Load Profiles
    ax2 = fig.add_subplot(gs[0, 1])
    
    for site_name in sites:
        load_name = f'Load_{site_name}'
        if load_name in n.loads.index:
            load_kw = n.loads_t.p_set[load_name].values * 1000
            ax2.plot(hours, load_kw, 's-', label=site_name, linewidth=2, markersize=4)
    
    ax2.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Load (kW)', fontsize=11, fontweight='bold')
    ax2.set_title('Host Load Profiles', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 23)
    
    # 3. Generation vs Load Balance
    ax3 = fig.add_subplot(gs[0, 2])
    
    total_gen = np.zeros(24)
    total_load = np.zeros(24)
    
    for site_name in sites:
        gen_name = f'Canopy_{site_name}'
        load_name = f'Load_{site_name}'
        if gen_name in n.generators.index:
            total_gen += n.generators_t.p[gen_name].values * 1000
        if load_name in n.loads.index:
            total_load += n.loads_t.p_set[load_name].values * 1000
    
    ax3.plot(hours, total_gen, 'g-', linewidth=3, label='Total Generation', marker='o')
    ax3.plot(hours, total_load, 'r-', linewidth=3, label='Total Load', marker='s')
    ax3.fill_between(hours, total_gen, total_load,
                    where=(total_gen >= total_load),
                    alpha=0.3, color='green', label='Surplus')
    ax3.fill_between(hours, total_gen, total_load,
                    where=(total_gen < total_load),
                    alpha=0.3, color='red', label='Deficit')
    
    ax3.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Power (kW)', fontsize=11, fontweight='bold')
    ax3.set_title('Generation vs Load Balance', fontsize=12, fontweight='bold')
    ax3.legend(framealpha=0.9)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 23)
    
    # 4. Battery Operation (Power)
    ax4 = fig.add_subplot(gs[0, 3])
    
    for site_name in sites:
        battery_name = f'Battery_{site_name}'
        if battery_name in n.storage_units.index:
            battery_p = n.storage_units_t.p[battery_name].values * 1000  # kW
            ax4.plot(hours, battery_p, 'o-', label=site_name, linewidth=2, markersize=4)
    
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Power (kW)\n(+)Discharge / (-)Charge', fontsize=11, fontweight='bold')
    ax4.set_title('Battery Operation (Optimized 0.5h)', fontsize=12, fontweight='bold')
    ax4.legend(framealpha=0.9)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 23)
    
    # 5. Battery State of Charge
    ax5 = fig.add_subplot(gs[1, 0])
    
    for site_name in sites:
        battery_name = f'Battery_{site_name}'
        if battery_name in n.storage_units.index:
            soc = n.storage_units_t.state_of_charge[battery_name].values
            max_soc = n.storage_units.loc[battery_name, 'p_nom'] * n.storage_units.loc[battery_name, 'max_hours']
            soc_pct = (soc / max_soc) * 100
            ax5.plot(hours, soc_pct, 'o-', label=site_name, linewidth=2, markersize=4)
    
    ax5.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax5.set_ylabel('State of Charge (%)', fontsize=11, fontweight='bold')
    ax5.set_title('Battery State of Charge', fontsize=12, fontweight='bold')
    ax5.legend(framealpha=0.9)
    ax5.grid(True, alpha=0.3)
    ax5.set_xlim(0, 23)
    ax5.set_ylim(0, 105)
    
    # 6. Grid Interaction
    ax6 = fig.add_subplot(gs[1, 1])
    
    if 'Grid_HOUSTON' in n.links.index:
        grid_p = n.links_t.p1['Grid_HOUSTON'].values * 1000  # Export (positive)
        grid_import = -n.links_t.p0['Grid_HOUSTON'].values * 1000  # Import (positive)
        
        ax6.plot(hours, grid_p, 'g-', linewidth=2, label='Grid Export', marker='o')
        ax6.plot(hours, grid_import, 'r-', linewidth=2, label='Grid Import', marker='s')
        ax6.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax6.fill_between(hours, 0, grid_p, alpha=0.3, color='green')
        ax6.fill_between(hours, 0, -grid_import, alpha=0.3, color='red')
    
    ax6.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Power (kW)', fontsize=11, fontweight='bold')
    ax6.set_title('Grid Interaction', fontsize=12, fontweight='bold')
    ax6.legend(framealpha=0.9)
    ax6.grid(True, alpha=0.3)
    ax6.set_xlim(0, 23)
    
    # 7. Scenario Comparison (Revenue)
    ax7 = fig.add_subplot(gs[1, 2])
    
    scenario_names = []
    revenues = []
    costs = []
    net_revenues = []
    
    for key, result in results.items():
        if result:
            scenario_names.append(result['scenario'])
            revenues.append(result.get('revenue', {}).get('total_revenue', 0))
            costs.append(result.get('costs', {}).get('total_cost', 0))
            net_revenues.append(result.get('net_revenue', 0))
    
    x_pos = np.arange(len(scenario_names))
    width = 0.35
    
    bars1 = ax7.bar(x_pos - width/2, revenues, width, label='Revenue', 
                   color='#4ECDC4', alpha=0.8, edgecolor='black')
    bars2 = ax7.bar(x_pos + width/2, costs, width, label='Costs',
                   color='#FF6B6B', alpha=0.8, edgecolor='black')
    
    ax7.set_xlabel('Scenario', fontsize=11, fontweight='bold')
    ax7.set_ylabel('Daily Value ($)', fontsize=11, fontweight='bold')
    ax7.set_title('Revenue vs Costs by Scenario', fontsize=12, fontweight='bold')
    ax7.set_xticks(x_pos)
    ax7.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax7.legend(framealpha=0.9)
    ax7.grid(True, alpha=0.3, axis='y')
    
    # 8. Energy Balance Summary
    ax8 = fig.add_subplot(gs[1, 3])
    ax8.axis('off')
    
    total_gen_kwh = np.sum(total_gen)
    total_load_kwh = np.sum(total_load)
    surplus = max(0, total_gen_kwh - total_load_kwh)
    deficit = max(0, total_load_kwh - total_gen_kwh)
    
    summary_text = f"""
    ENERGY BALANCE SUMMARY
    {'='*40}
    
    Total Generation: {total_gen_kwh:.1f} kWh
    Total Load: {total_load_kwh:.1f} kWh
    
    Surplus: {surplus:.1f} kWh
    Deficit: {deficit:.1f} kWh
    
    Self-Consumption: {min(total_gen_kwh, total_load_kwh):.1f} kWh
    Self-Consumption Rate: {min(total_gen_kwh, total_load_kwh)/total_gen_kwh*100:.1f}%
    
    Battery Capacity: {OPTIMIZED_CONFIG['total_battery_kw']} kW / {OPTIMIZED_CONFIG['total_battery_kwh']} kWh
    Battery Duration: {OPTIMIZED_CONFIG['battery_config']['duration_hours']:.1f} hours
    """
    
    ax8.text(0.1, 0.9, summary_text, transform=ax8.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    # 9. Hourly Energy Flow (Stacked)
    ax9 = fig.add_subplot(gs[2, 0:2])
    
    # Stack generation sources
    gen_stack = np.zeros(24)
    for site_name in sites:
        gen_name = f'Canopy_{site_name}'
        if gen_name in n.generators.index:
            gen_kw = n.generators_t.p[gen_name].values * 1000
            ax9.fill_between(hours, gen_stack, gen_stack + gen_kw,
                           label=site_name, alpha=0.7)
            gen_stack += gen_kw
    
    # Add battery discharge
    battery_discharge = np.zeros(24)
    for site_name in sites:
        battery_name = f'Battery_{site_name}'
        if battery_name in n.storage_units.index:
            battery_p = n.storage_units_t.p[battery_name].values * 1000
            battery_discharge += np.maximum(0, battery_p)
    
    if np.sum(battery_discharge) > 0:
        ax9.fill_between(hours, gen_stack, gen_stack + battery_discharge,
                       label='Battery Discharge', alpha=0.7, color='orange')
        gen_stack += battery_discharge
    
    # Add grid import
    if 'Grid_HOUSTON' in n.links.index:
        grid_import = -n.links_t.p0['Grid_HOUSTON'].values * 1000
        grid_import = np.maximum(0, grid_import)
        if np.sum(grid_import) > 0:
            ax9.fill_between(hours, gen_stack, gen_stack + grid_import,
                           label='Grid Import', alpha=0.7, color='gray')
    
    ax9.plot(hours, total_load, 'r-', linewidth=3, label='Total Load', marker='s')
    
    ax9.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
    ax9.set_ylabel('Power (kW)', fontsize=11, fontweight='bold')
    ax9.set_title('Hourly Energy Flow (Stacked)', fontsize=12, fontweight='bold')
    ax9.legend(loc='upper right', framealpha=0.9)
    ax9.grid(True, alpha=0.3)
    ax9.set_xlim(0, 23)
    
    # 10. Revenue Breakdown
    ax10 = fig.add_subplot(gs[2, 2])
    
    if s1.get('revenue'):
        rev = s1['revenue']
        revenue_sources = ['PPA', 'Grid']
        revenue_values = [rev.get('ppa_revenue', 0), rev.get('grid_revenue', 0)]
        
        colors = ['#4ECDC4', '#45B7D1']
        bars = ax10.bar(revenue_sources, revenue_values, color=colors, alpha=0.8,
                       edgecolor='black', linewidth=1.5)
        ax10.set_ylabel('Daily Revenue ($)', fontsize=11, fontweight='bold')
        ax10.set_title('Revenue Breakdown (S1)', fontsize=12, fontweight='bold')
        ax10.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, revenue_values):
            if val > 0:
                height = bar.get_height()
                ax10.text(bar.get_x() + bar.get_width()/2., height,
                         f'${val:.0f}', ha='center', va='bottom',
                         fontsize=10, fontweight='bold')
    
    # 11. Battery Energy Throughput
    ax11 = fig.add_subplot(gs[2, 3])
    
    battery_throughput = {}
    for site_name in sites:
        battery_name = f'Battery_{site_name}'
        if battery_name in n.storage_units.index:
            battery_p = n.storage_units_t.p[battery_name].values * 1000  # kW
            charge_energy = np.sum(np.maximum(0, -battery_p))  # kWh charged
            discharge_energy = np.sum(np.maximum(0, battery_p))  # kWh discharged
            battery_throughput[site_name] = {
                'charge': charge_energy,
                'discharge': discharge_energy,
                'total': charge_energy + discharge_energy
            }
    
    if battery_throughput:
        site_names = list(battery_throughput.keys())
        throughput_values = [battery_throughput[s]['total'] for s in site_names]
        
        bars = ax11.bar(site_names, throughput_values, color='#FFA07A', alpha=0.8,
                       edgecolor='black', linewidth=1.5)
        ax11.set_ylabel('Energy Throughput (kWh)', fontsize=11, fontweight='bold')
        ax11.set_title('Battery Energy Throughput', fontsize=12, fontweight='bold')
        ax11.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, throughput_values):
            height = bar.get_height()
            ax11.text(bar.get_x() + bar.get_width()/2., height,
                     f'{val:.0f}', ha='center', va='bottom',
                     fontsize=10, fontweight='bold')
    
    # 12. System Configuration Summary
    ax12 = fig.add_subplot(gs[3, 0:2])
    ax12.axis('off')
    
    config_text = f"""
    OPTIMIZED SYSTEM CONFIGURATION
    {'='*60}
    
    Solar Capacity: {OPTIMIZED_CONFIG['total_solar_kw']} kW
        Site A: {OPTIMIZED_CONFIG['sites']['Site_A']['solar_kw']} kW
        Site B: {OPTIMIZED_CONFIG['sites']['Site_B']['solar_kw']} kW
        Site C: {OPTIMIZED_CONFIG['sites']['Site_C']['solar_kw']} kW
    
    Battery Capacity: {OPTIMIZED_CONFIG['total_battery_kw']} kW / {OPTIMIZED_CONFIG['total_battery_kwh']} kWh
        Site A: {OPTIMIZED_CONFIG['sites']['Site_A']['battery_kw']} kW / {OPTIMIZED_CONFIG['sites']['Site_A']['battery_kwh']} kWh
        Site B: {OPTIMIZED_CONFIG['sites']['Site_B']['battery_kw']} kW / {OPTIMIZED_CONFIG['sites']['Site_B']['battery_kwh']} kWh
        Site C: {OPTIMIZED_CONFIG['sites']['Site_C']['battery_kw']} kW / {OPTIMIZED_CONFIG['sites']['Site_C']['battery_kwh']} kWh
        Duration: {OPTIMIZED_CONFIG['battery_config']['duration_hours']:.1f} hours
    
    PPA Rate: {get_optimized_ppa_rate():.2f}¢/kWh
    Net CAPEX: ${get_optimized_capex()/1e6:.2f}M (No ITC)
    
    Annual Generation: {OPTIMIZED_CONFIG['annual_generation_mwh']} MWh
    Annual Revenue: ${get_optimized_revenue_streams()['total']/1e3:.0f}k
    """
    
    ax12.text(0.05, 0.95, config_text, transform=ax12.transAxes,
             fontsize=10, verticalalignment='top', family='monospace',
             bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.8))
    
    # 13. Financial Metrics Summary
    ax13 = fig.add_subplot(gs[3, 2:])
    ax13.axis('off')
    
    from capex_analysis import calculate_financial_metrics
    
    rev = get_optimized_revenue_streams()
    capex = get_optimized_capex()
    metrics = calculate_financial_metrics(
        rev['total'], OPTIMIZED_CONFIG['annual_opex_usd'], capex, 25, 0.08
    )
    
    financial_text = f"""
    FINANCIAL METRICS (Optimized, No ITC)
    {'='*60}
    
    Revenue Streams:
        Base PPA: ${rev['base_ppa']/1e3:.0f}k/year
        Platform Fees: ${rev['platform_fees']/1e3:.0f}k/year
        Grid Services: ${rev['grid_services']/1e3:.0f}k/year
        EV Charging: ${rev['ev_charging']/1e3:.0f}k/year
        REC Sales: ${rev['rec_sales']/1e3:.0f}k/year
        Digital Twin: ${rev.get('digital_twin_licensing', 0)/1e3:.0f}k/year
        Total: ${rev['total']/1e3:.0f}k/year
    
    Financial Metrics:
        Net CAPEX: ${capex/1e6:.2f}M
        Annual OPEX: ${OPTIMIZED_CONFIG['annual_opex_usd']/1e3:.0f}k
        Annual Cash Flow: ${metrics['annual_cash_flow']/1e3:.0f}k
        
        IRR: {metrics['irr']*100:.1f}%
        Payback: {metrics['payback_years']:.1f} years
        NPV: ${metrics['npv']/1e6:.2f}M
        ROI: {metrics['roi']:.1f}%
    """
    
    ax13.text(0.05, 0.95, financial_text, transform=ax13.transAxes,
             fontsize=10, verticalalignment='top', family='monospace',
             bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8))
    
    plt.suptitle('Optimized PyPSA Scenario Analysis\n' + 
                'Comprehensive Outputs: Loads, Generation, Battery, Optimization',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Comprehensive PyPSA outputs saved to: {save_path}")
    
    return fig


def plot_load_analysis(results, save_path='visualizations/optimized_pypsa_loads.png'):
    """
    Detailed load analysis visualization.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    s1 = results.get('S1')
    if s1 is None:
        return None
    
    n = s1['network']
    sites = ['Site_A', 'Site_B', 'Site_C']
    hours = np.arange(24)
    
    # 1. Individual Load Profiles
    ax1 = fig.add_subplot(gs[0, 0])
    
    for site_name in sites:
        load_name = f'Load_{site_name}'
        if load_name in n.loads.index:
            load_kw = n.loads_t.p_set[load_name].values * 1000
            ax1.plot(hours, load_kw, 'o-', label=site_name, linewidth=2.5, markersize=6)
    
    ax1.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Load (kW)', fontsize=12, fontweight='bold')
    ax1.set_title('Individual Site Load Profiles', fontsize=13, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 23)
    
    # 2. Total Load Profile
    ax2 = fig.add_subplot(gs[0, 1])
    
    total_load = np.zeros(24)
    for site_name in sites:
        load_name = f'Load_{site_name}'
        if load_name in n.loads.index:
            total_load += n.loads_t.p_set[load_name].values * 1000
    
    ax2.fill_between(hours, 0, total_load, alpha=0.6, color='#FF6B6B')
    ax2.plot(hours, total_load, 'r-', linewidth=3, marker='o', markersize=6)
    ax2.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Total Load (kW)', fontsize=12, fontweight='bold')
    ax2.set_title('Total System Load Profile', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 23)
    
    # 3. Load Statistics
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis('off')
    
    load_stats = {}
    for site_name in sites:
        load_name = f'Load_{site_name}'
        if load_name in n.loads.index:
            load_kw = n.loads_t.p_set[load_name].values * 1000
            load_stats[site_name] = {
                'peak': np.max(load_kw),
                'average': np.mean(load_kw),
                'min': np.min(load_kw),
                'total': np.sum(load_kw)
            }
    
    stats_text = "LOAD STATISTICS\n" + "="*40 + "\n\n"
    for site_name, stats in load_stats.items():
        stats_text += f"{site_name}:\n"
        stats_text += f"  Peak: {stats['peak']:.1f} kW\n"
        stats_text += f"  Average: {stats['average']:.1f} kW\n"
        stats_text += f"  Minimum: {stats['min']:.1f} kW\n"
        stats_text += f"  Daily Total: {stats['total']:.1f} kWh\n\n"
    
    total_stats = {
        'peak': np.max(total_load),
        'average': np.mean(total_load),
        'min': np.min(total_load),
        'total': np.sum(total_load)
    }
    
    stats_text += "TOTAL SYSTEM:\n"
    stats_text += f"  Peak: {total_stats['peak']:.1f} kW\n"
    stats_text += f"  Average: {total_stats['average']:.1f} kW\n"
    stats_text += f"  Minimum: {total_stats['min']:.1f} kW\n"
    stats_text += f"  Daily Total: {total_stats['total']:.1f} kWh\n"
    stats_text += f"  Load Factor: {total_stats['average']/total_stats['peak']*100:.1f}%"
    
    ax3.text(0.1, 0.95, stats_text, transform=ax3.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    # 4. Load Duration Curve
    ax4 = fig.add_subplot(gs[1, 0])
    
    sorted_load = np.sort(total_load)[::-1]  # Descending
    ax4.plot(range(24), sorted_load, 'r-', linewidth=3, marker='o', markersize=5)
    ax4.fill_between(range(24), 0, sorted_load, alpha=0.6, color='#FF6B6B')
    ax4.set_xlabel('Hour Rank (Highest to Lowest)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Load (kW)', fontsize=12, fontweight='bold')
    ax4.set_title('Load Duration Curve', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. Load vs Generation Match
    ax5 = fig.add_subplot(gs[1, 1])
    
    total_gen = np.zeros(24)
    for site_name in sites:
        gen_name = f'Canopy_{site_name}'
        if gen_name in n.generators.index:
            total_gen += n.generators_t.p[gen_name].values * 1000
    
    match_ratio = np.minimum(total_gen, total_load) / np.maximum(total_gen, total_load)
    match_ratio = np.nan_to_num(match_ratio)
    
    ax5.plot(hours, match_ratio * 100, 'o-', linewidth=3, markersize=6, color='#4ECDC4')
    ax5.axhline(y=100, color='g', linestyle='--', linewidth=2, label='Perfect Match')
    ax5.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Match Ratio (%)', fontsize=12, fontweight='bold')
    ax5.set_title('Load-Generation Match Quality', fontsize=13, fontweight='bold')
    ax5.legend(framealpha=0.9)
    ax5.grid(True, alpha=0.3)
    ax5.set_xlim(0, 23)
    ax5.set_ylim(0, 105)
    
    # 6. Load Profile Comparison (Stacked)
    ax6 = fig.add_subplot(gs[1, 2])
    
    load_stack = np.zeros(24)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    for i, site_name in enumerate(sites):
        load_name = f'Load_{site_name}'
        if load_name in n.loads.index:
            load_kw = n.loads_t.p_set[load_name].values * 1000
            ax6.fill_between(hours, load_stack, load_stack + load_kw,
                           label=site_name, alpha=0.7, color=colors[i])
            load_stack += load_kw
    
    ax6.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Load (kW)', fontsize=12, fontweight='bold')
    ax6.set_title('Stacked Load Profiles', fontsize=13, fontweight='bold')
    ax6.legend(framealpha=0.9)
    ax6.grid(True, alpha=0.3)
    ax6.set_xlim(0, 23)
    
    # 7-9. Load characteristics
    # Peak hours
    ax7 = fig.add_subplot(gs[2, 0])
    
    peak_hours = np.argmax(total_load)
    ax7.bar(['Peak Hour'], [peak_hours], color='#FF6B6B', alpha=0.8, edgecolor='black')
    ax7.set_ylabel('Hour of Day', fontsize=12, fontweight='bold')
    ax7.set_title('Peak Load Hour', fontsize=13, fontweight='bold')
    ax7.set_ylim(0, 23)
    ax7.text(0, peak_hours, f'Hour {peak_hours}', ha='center', va='bottom',
            fontsize=12, fontweight='bold')
    
    # Load factor
    ax8 = fig.add_subplot(gs[2, 1])
    
    load_factor = total_stats['average'] / total_stats['peak'] * 100
    ax8.bar(['Load Factor'], [load_factor], color='#4ECDC4', alpha=0.8, edgecolor='black')
    ax8.set_ylabel('Load Factor (%)', fontsize=12, fontweight='bold')
    ax8.set_title('System Load Factor', fontsize=13, fontweight='bold')
    ax8.set_ylim(0, 100)
    ax8.text(0, load_factor, f'{load_factor:.1f}%', ha='center', va='bottom',
            fontsize=12, fontweight='bold')
    
    # Daily energy
    ax9 = fig.add_subplot(gs[2, 2])
    
    daily_energy = total_stats['total']
    ax9.bar(['Daily Energy'], [daily_energy/1000], color='#45B7D1', alpha=0.8, edgecolor='black')
    ax9.set_ylabel('Daily Energy (MWh)', fontsize=12, fontweight='bold')
    ax9.set_title('Total Daily Load Energy', fontsize=13, fontweight='bold')
    ax9.text(0, daily_energy/1000, f'{daily_energy/1000:.2f} MWh', ha='center', va='bottom',
            fontsize=12, fontweight='bold')
    
    plt.suptitle('Optimized PyPSA Load Analysis\n' + 
                'Detailed Load Profiles and Characteristics',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Load analysis saved to: {save_path}")
    
    return fig


def plot_optimization_details(results, save_path='visualizations/optimized_pypsa_optimization.png'):
    """
    Detailed optimization analysis.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    s1 = results.get('S1')
    s2 = results.get('S2')
    
    if s1 is None:
        return None
    
    n1 = s1['network']
    sites = ['Site_A', 'Site_B', 'Site_C']
    hours = np.arange(24)
    
    # 1. Optimization Objective (Cost Minimization)
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Calculate hourly costs
    hourly_costs = []
    for h in hours:
        # Grid import cost
        if 'Grid_HOUSTON' in n1.links.index:
            grid_import = -n1.links_t.p0['Grid_HOUSTON'].iloc[h] * 1000  # kW
            lmp = 50 / 1000  # $/kWh (simplified)
            cost = max(0, grid_import) * lmp
            hourly_costs.append(cost)
        else:
            hourly_costs.append(0)
    
    ax1.bar(hours, hourly_costs, color='#FF6B6B', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cost ($)', fontsize=12, fontweight='bold')
    ax1.set_title('Hourly System Cost (S1)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_xlim(-0.5, 23.5)
    
    # 2. Battery Optimization Strategy
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Show battery arbitrage (charge during low price, discharge during high)
    battery_p_total = np.zeros(24)
    for site_name in sites:
        battery_name = f'Battery_{site_name}'
        if battery_name in n1.storage_units.index:
            battery_p = n1.storage_units_t.p[battery_name].values * 1000
            battery_p_total += battery_p
    
    ax2.plot(hours, battery_p_total, 'o-', linewidth=3, markersize=6, color='#4ECDC4')
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax2.fill_between(hours, 0, battery_p_total, where=(battery_p_total > 0),
                     alpha=0.3, color='green', label='Discharge')
    ax2.fill_between(hours, 0, battery_p_total, where=(battery_p_total < 0),
                     alpha=0.3, color='red', label='Charge')
    ax2.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Total Battery Power (kW)', fontsize=12, fontweight='bold')
    ax2.set_title('Battery Optimization Strategy', fontsize=13, fontweight='bold')
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 23)
    
    # 3. Power Balance (Generation + Battery + Grid = Load)
    ax3 = fig.add_subplot(gs[0, 2])
    
    total_gen = np.zeros(24)
    for site_name in sites:
        gen_name = f'Canopy_{site_name}'
        if gen_name in n1.generators.index:
            total_gen += n1.generators_t.p[gen_name].values * 1000
    
    total_load = np.zeros(24)
    for site_name in sites:
        load_name = f'Load_{site_name}'
        if load_name in n1.loads.index:
            total_load += n1.loads_t.p_set[load_name].values * 1000
    
    battery_discharge = np.maximum(0, battery_p_total)
    grid_import = np.zeros(24)
    if 'Grid_HOUSTON' in n1.links.index:
        grid_import = np.maximum(0, -n1.links_t.p0['Grid_HOUSTON'].values * 1000)
    
    supply = total_gen + battery_discharge + grid_import
    
    ax3.plot(hours, supply, 'g-', linewidth=3, label='Supply', marker='o')
    ax3.plot(hours, total_load, 'r-', linewidth=3, label='Demand', marker='s')
    ax3.fill_between(hours, supply, total_load, alpha=0.3, color='yellow')
    ax3.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Power (kW)', fontsize=12, fontweight='bold')
    ax3.set_title('Power Balance (Optimized)', fontsize=13, fontweight='bold')
    ax3.legend(framealpha=0.9)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 23)
    
    # 4. Scenario Comparison (Optimization Results)
    ax4 = fig.add_subplot(gs[1, 0])
    
    scenario_names = []
    net_revenues = []
    total_revenues = []
    
    for key, result in results.items():
        if result:
            scenario_names.append(result['scenario'])
            net_revenues.append(result.get('net_revenue', 0))
            total_revenues.append(result.get('revenue', {}).get('total_revenue', 0))
    
    x_pos = np.arange(len(scenario_names))
    width = 0.35
    
    bars1 = ax4.bar(x_pos - width/2, total_revenues, width, label='Total Revenue',
                   color='#4ECDC4', alpha=0.8, edgecolor='black')
    bars2 = ax4.bar(x_pos + width/2, net_revenues, width, label='Net Revenue',
                   color='#45B7D1', alpha=0.8, edgecolor='black')
    
    ax4.set_xlabel('Scenario', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Daily Revenue ($)', fontsize=12, fontweight='bold')
    ax4.set_title('Optimization Results by Scenario', fontsize=13, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax4.legend(framealpha=0.9)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Battery Utilization
    ax5 = fig.add_subplot(gs[1, 1])
    
    battery_utilization = {}
    for site_name in sites:
        battery_name = f'Battery_{site_name}'
        if battery_name in n1.storage_units.index:
            battery_p = n1.storage_units_t.p[battery_name].values * 1000
            max_power = n1.storage_units.loc[battery_name, 'p_nom'] * 1000
            utilization = np.abs(battery_p) / max_power * 100
            battery_utilization[site_name] = np.mean(utilization)
    
    if battery_utilization:
        site_names = list(battery_utilization.keys())
        util_values = list(battery_utilization.values())
        
        bars = ax5.bar(site_names, util_values, color='#FFA07A', alpha=0.8,
                       edgecolor='black', linewidth=1.5)
        ax5.set_ylabel('Average Utilization (%)', fontsize=12, fontweight='bold')
        ax5.set_title('Battery Utilization (Optimized)', fontsize=13, fontweight='bold')
        ax5.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, util_values):
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}%', ha='center', va='bottom',
                    fontsize=10, fontweight='bold')
    
    # 6. Energy Flow Sankey-style (simplified)
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    total_gen_kwh = np.sum(total_gen)
    total_load_kwh = np.sum(total_load)
    battery_charge_kwh = np.sum(np.maximum(0, -battery_p_total))
    battery_discharge_kwh = np.sum(np.maximum(0, battery_p_total))
    
    flow_text = f"""
    ENERGY FLOW SUMMARY
    {'='*50}
    
    Generation: {total_gen_kwh:.1f} kWh
    
    Uses:
        Direct to Load: {min(total_gen_kwh, total_load_kwh):.1f} kWh
        Battery Charge: {battery_charge_kwh:.1f} kWh
        Grid Export: {max(0, total_gen_kwh - total_load_kwh - battery_charge_kwh):.1f} kWh
    
    Load: {total_load_kwh:.1f} kWh
    
    Sources:
        Direct from Solar: {min(total_gen_kwh, total_load_kwh):.1f} kWh
        Battery Discharge: {battery_discharge_kwh:.1f} kWh
        Grid Import: {max(0, total_load_kwh - total_gen_kwh - battery_discharge_kwh):.1f} kWh
    
    Battery Round-Trip Efficiency: 90.25%
    (95% charge × 95% discharge)
    """
    
    ax6.text(0.1, 0.9, flow_text, transform=ax6.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.8))
    
    # 7-9. Optimization metrics
    # Self-consumption
    ax7 = fig.add_subplot(gs[2, 0])
    
    self_consumption = min(total_gen_kwh, total_load_kwh)
    self_consumption_rate = self_consumption / total_gen_kwh * 100 if total_gen_kwh > 0 else 0
    
    ax7.bar(['Self-Consumption'], [self_consumption_rate], color='#4ECDC4', alpha=0.8, edgecolor='black')
    ax7.set_ylabel('Rate (%)', fontsize=12, fontweight='bold')
    ax7.set_title('Self-Consumption Rate', fontsize=13, fontweight='bold')
    ax7.set_ylim(0, 100)
    ax7.text(0, self_consumption_rate, f'{self_consumption_rate:.1f}%', ha='center', va='bottom',
            fontsize=12, fontweight='bold')
    
    # Grid independence
    ax8 = fig.add_subplot(gs[2, 1])
    
    grid_independence = (1 - max(0, total_load_kwh - total_gen_kwh - battery_discharge_kwh) / total_load_kwh) * 100 if total_load_kwh > 0 else 0
    grid_independence = max(0, min(100, grid_independence))
    
    ax8.bar(['Grid Independence'], [grid_independence], color='#45B7D1', alpha=0.8, edgecolor='black')
    ax8.set_ylabel('Rate (%)', fontsize=12, fontweight='bold')
    ax8.set_title('Grid Independence', fontsize=13, fontweight='bold')
    ax8.set_ylim(0, 100)
    ax8.text(0, grid_independence, f'{grid_independence:.1f}%', ha='center', va='bottom',
            fontsize=12, fontweight='bold')
    
    # Optimization efficiency
    ax9 = fig.add_subplot(gs[2, 2])
    
    # Calculate how well optimization minimized costs
    optimal_cost = s1.get('costs', {}).get('total_cost', 0)
    # Compare to naive dispatch (no optimization)
    naive_cost = total_load_kwh * 0.15  # Assume 15¢/kWh retail
    optimization_savings = (naive_cost - optimal_cost) / naive_cost * 100 if naive_cost > 0 else 0
    
    ax9.bar(['Cost Savings'], [optimization_savings], color='#FFA07A', alpha=0.8, edgecolor='black')
    ax9.set_ylabel('Savings (%)', fontsize=12, fontweight='bold')
    ax9.set_title('Optimization Cost Savings', fontsize=13, fontweight='bold')
    ax9.set_ylim(0, 100)
    ax9.text(0, optimization_savings, f'{optimization_savings:.1f}%', ha='center', va='bottom',
            fontsize=12, fontweight='bold')
    
    plt.suptitle('Optimized PyPSA Optimization Analysis\n' + 
                'Detailed Optimization Results and Metrics',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Optimization details saved to: {save_path}")
    
    return fig


if __name__ == "__main__":
    from run_optimized_pypsa_scenarios import run_all_optimized_scenarios
    
    print("Running optimized PyPSA scenarios...")
    results = run_all_optimized_scenarios()
    
    print("\nGenerating comprehensive visualizations...")
    plot_comprehensive_pypsa_outputs(results)
    plot_load_analysis(results)
    plot_optimization_details(results)
    
    print("\nAll PyPSA visualizations generated!")

