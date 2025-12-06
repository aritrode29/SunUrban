"""
Optimized Scenario Visualizations
=================================

Creates visualizations using optimized parameters from IRR optimizer.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
import sys
sys.path.insert(0, 'pypsa_models')

from optimized_scenario_config import (
    OPTIMIZED_CONFIG, COMPARISON,
    get_optimized_ppa_rate,
    get_optimized_capex,
    get_optimized_revenue_streams
)
from capex_analysis import calculate_financial_metrics
import warnings
warnings.filterwarnings('ignore')


def plot_optimized_financial_comparison(save_path='visualizations/optimized_financial_comparison.png'):
    """
    Compare original vs optimized financial metrics.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    comp = COMPARISON
    
    # 1. IRR Comparison
    ax1 = fig.add_subplot(gs[0, 0])
    
    scenarios = ['Original', 'Optimized']
    irr_values = [comp['irr']['original'], comp['irr']['optimized']]
    colors = ['#FF6B6B', '#4ECDC4']
    
    bars = ax1.bar(scenarios, irr_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2)
    ax1.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax1.set_ylabel('IRR (%)', fontsize=12, fontweight='bold')
    ax1.set_title('IRR: Original vs Optimized', fontsize=13, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, irr_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom',
                fontsize=12, fontweight='bold')
    
    # 2. CAPEX Comparison
    ax2 = fig.add_subplot(gs[0, 1])
    
    capex_values = [comp['net_capex']['original']/1e6, comp['net_capex']['optimized']/1e6]
    bars = ax2.bar(scenarios, capex_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2)
    ax2.set_ylabel('Net CAPEX ($M)', fontsize=12, fontweight='bold')
    ax2.set_title('CAPEX: Original vs Optimized', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, capex_values):
        height = bar.get_height()
        reduction = (1 - comp['net_capex']['optimized']/comp['net_capex']['original']) * 100
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'${val:.2f}M\n(-{reduction:.0f}%)' if bar == bars[1] else f'${val:.2f}M',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 3. Revenue Comparison
    ax3 = fig.add_subplot(gs[0, 2])
    
    revenue_values = [comp['annual_revenue']['original']/1e3, comp['annual_revenue']['optimized']/1e3]
    bars = ax3.bar(scenarios, revenue_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2)
    ax3.set_ylabel('Annual Revenue ($1000s)', fontsize=12, fontweight='bold')
    ax3.set_title('Revenue: Original vs Optimized', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, revenue_values):
        height = bar.get_height()
        increase = (comp['annual_revenue']['optimized']/comp['annual_revenue']['original'] - 1) * 100
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'${val:.0f}k\n(+{increase:.0f}%)' if bar == bars[1] else f'${val:.0f}k',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 4. Payback Comparison
    ax4 = fig.add_subplot(gs[1, 0])
    
    payback_values = [comp['payback']['original'], comp['payback']['optimized']]
    bars = ax4.bar(scenarios, payback_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2)
    ax4.set_ylabel('Payback Period (years)', fontsize=12, fontweight='bold')
    ax4.set_title('Payback: Original vs Optimized', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, payback_values):
        height = bar.get_height()
        improvement = (1 - comp['payback']['optimized']/comp['payback']['original']) * 100
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}y\n(-{improvement:.0f}%)' if bar == bars[1] else f'{val:.1f}y',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 5. Revenue Streams Breakdown
    ax5 = fig.add_subplot(gs[1, 1])
    
    rev = get_optimized_revenue_streams()
    revenue_sources = ['Base PPA', 'Platform\nFees', 'Grid\nServices', 'EV\nCharging', 'REC\nSales']
    revenue_values = [
        rev['base_ppa']/1e3,
        rev['platform_fees']/1e3,
        rev['grid_services']/1e3,
        rev['ev_charging']/1e3,
        rev['rec_sales']/1e3
    ]
    
    colors_rev = ['#4ECDC4', '#FFD700', '#45B7D1', '#FFA07A', '#98D8C8']
    bars = ax5.bar(revenue_sources, revenue_values, color=colors_rev, alpha=0.8,
                  edgecolor='black', linewidth=1.5)
    ax5.set_ylabel('Revenue ($1000s)', fontsize=12, fontweight='bold')
    ax5.set_title('Optimized Revenue Streams', fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, revenue_values):
        if val > 0:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'${val:.0f}k', ha='center', va='bottom',
                    fontsize=10, fontweight='bold')
    
    # 6. Battery Configuration Comparison
    ax6 = fig.add_subplot(gs[1, 2])
    
    battery_metrics = ['Power\n(kW)', 'Energy\n(kWh)', 'Duration\n(hours)']
    original_values = [
        comp['battery_power']['original'],
        comp['battery_energy']['original'],
        comp['battery_duration']['original']
    ]
    optimized_values = [
        comp['battery_power']['optimized'],
        comp['battery_energy']['optimized'],
        comp['battery_duration']['optimized']
    ]
    
    x_pos = np.arange(len(battery_metrics))
    width = 0.35
    
    bars1 = ax6.bar(x_pos - width/2, original_values, width,
                   label='Original', color='#FF6B6B', alpha=0.8, edgecolor='black')
    bars2 = ax6.bar(x_pos + width/2, optimized_values, width,
                   label='Optimized', color='#4ECDC4', alpha=0.8, edgecolor='black')
    
    ax6.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax6.set_title('Battery Configuration Comparison', fontsize=13, fontweight='bold')
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(battery_metrics)
    ax6.legend(framealpha=0.9)
    ax6.grid(True, alpha=0.3, axis='y')
    
    # 7. PPA Rate Comparison
    ax7 = fig.add_subplot(gs[2, 0])
    
    ppa_values = [comp['ppa_rate']['original'], comp['ppa_rate']['optimized']]
    bars = ax7.bar(scenarios, ppa_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2)
    ax7.set_ylabel('PPA Rate (cents/kWh)', fontsize=12, fontweight='bold')
    ax7.set_title('PPA Rate: Original vs Optimized', fontsize=13, fontweight='bold')
    ax7.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, ppa_values):
        height = bar.get_height()
        change = comp['ppa_rate']['change_pct']
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}c\n({change:+.1f}%)' if bar == bars[1] else f'{val:.2f}c',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 8. Financial Metrics Summary
    ax8 = fig.add_subplot(gs[2, 1:])
    ax8.axis('off')
    
    # Calculate NPV
    original_revenue = comp['annual_revenue']['original']
    optimized_revenue = comp['annual_revenue']['optimized']
    annual_opex = 43000
    
    original_metrics = calculate_financial_metrics(
        original_revenue, annual_opex, comp['net_capex']['original'],
        25, 0.08
    )
    optimized_metrics = calculate_financial_metrics(
        optimized_revenue, annual_opex, comp['net_capex']['optimized'],
        25, 0.08
    )
    
    summary_text = f"""
    FINANCIAL METRICS SUMMARY
    {'='*70}
    
    Original Configuration:
        PPA Rate: {comp['ppa_rate']['original']:.2f}c/kWh
        Net CAPEX: ${comp['net_capex']['original']/1e6:.2f}M
        Annual Revenue: ${comp['annual_revenue']['original']/1e3:.0f}k
        IRR: {comp['irr']['original']:.1f}%
        Payback: {comp['payback']['original']:.1f} years
        NPV: ${original_metrics['npv']/1e6:.2f}M
    
    Optimized Configuration:
        PPA Rate: {comp['ppa_rate']['optimized']:.2f}c/kWh (market-competitive)
        Net CAPEX: ${comp['net_capex']['optimized']/1e6:.2f}M (-{comp['net_capex']['change_pct']:.0f}% reduction)
        Annual Revenue: ${comp['annual_revenue']['optimized']/1e3:.0f}k (+{comp['annual_revenue']['change_pct']:.0f}% increase)
        IRR: {comp['irr']['optimized']:.1f}% (+{comp['irr']['change_pct']:.0f}% improvement)
        Payback: {comp['payback']['optimized']:.1f} years (-{abs(comp['payback']['change_pct']):.0f}% improvement)
        NPV: ${optimized_metrics['npv']/1e6:.2f}M
    
    Key Improvements:
        - CAPEX reduced by {comp['net_capex']['change_pct']:.0f}% (battery optimization + scale)
        - Revenue increased by {comp['annual_revenue']['change_pct']:.0f}% (multiple streams)
        - IRR improved from {comp['irr']['original']:.1f}% to {comp['irr']['optimized']:.1f}%
        - Payback reduced from {comp['payback']['original']:.1f} to {comp['payback']['optimized']:.1f} years
    """
    
    ax8.text(0.05, 0.95, summary_text, transform=ax8.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8))
    
    plt.suptitle('Optimized Scenario Financial Comparison\n' + 
                'Original vs Optimized Configuration',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Optimized financial comparison saved to: {save_path}")
    
    return fig


def plot_optimized_network_topology(save_path='visualizations/optimized_network_topology.png'):
    """
    Plot network topology with optimized battery sizes.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    # Bus positions
    positions = {
        'HOUSTON': (0.6, 0.3),
        'NORTH': (0.4, 0.7),
        'SOUTH': (0.2, 0.2),
        'WEST': (0.1, 0.5)
    }
    
    # Draw lines
    lines = [
        ('HOUSTON', 'NORTH', 2000),
        ('HOUSTON', 'SOUTH', 1500),
        ('NORTH', 'WEST', 1000),
        ('SOUTH', 'WEST', 800)
    ]
    
    for bus0, bus1, capacity in lines:
        pos0 = positions[bus0]
        pos1 = positions[bus1]
        ax.plot([pos0[0], pos1[0]], [pos0[1], pos1[1]], 
                'k-', linewidth=2, alpha=0.5, zorder=1)
        mid_x = (pos0[0] + pos1[0]) / 2
        mid_y = (pos0[1] + pos1[1]) / 2
        ax.text(mid_x, mid_y, f'{capacity} MW', 
                fontsize=8, ha='center', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Draw buses
    for bus_name, pos in positions.items():
        color = '#FF6B6B' if bus_name == 'HOUSTON' else '#4ECDC4'
        ax.scatter(pos[0], pos[1], s=1000, c=color, 
                  edgecolors='black', linewidths=2, zorder=2, alpha=0.8)
        ax.text(pos[0], pos[1], bus_name, 
                fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Add canopy sites with optimized battery sizes
    sites = OPTIMIZED_CONFIG['sites']
    canopies = [
        (f'Canopy SoCo\n{sites["Site_A"]["solar_kw"]} kW Solar\n{sites["Site_A"]["battery_kw"]} kW / {sites["Site_A"]["battery_kwh"]} kWh Battery', 
         0.72, 0.35),
        (f'Canopy Campus\n{sites["Site_B"]["solar_kw"]} kW Solar\n{sites["Site_B"]["battery_kw"]} kW / {sites["Site_B"]["battery_kwh"]} kWh Battery', 
         0.65, 0.22),
        (f'Canopy Airport\n{sites["Site_C"]["solar_kw"]} kW Solar\n{sites["Site_C"]["battery_kw"]} kW / {sites["Site_C"]["battery_kwh"]} kWh Battery', 
         0.75, 0.25)
    ]
    
    for name, x, y in canopies:
        ax.scatter(x, y, s=400, c='#FFD93D', marker='s',
                  edgecolors='black', linewidths=1.5, zorder=3, alpha=0.9)
        ax.text(x, y-0.1, name, fontsize=8, ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFD93D', alpha=0.7))
        ax.plot([0.6, x], [0.3, y], 'k--', linewidth=1, alpha=0.3)
    
    ax.set_xlim(-0.05, 0.9)
    ax.set_ylim(0.05, 0.85)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('ERCOT-Lite Network Topology (Optimized)\n' + 
                '4 Buses + 3 Solar Canopy Sites with Optimized Battery Sizing',
                fontsize=14, fontweight='bold', pad=20)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#FF6B6B', edgecolor='black', label='HOUSTON Bus (DER hub)'),
        mpatches.Patch(facecolor='#4ECDC4', edgecolor='black', label='Other Buses'),
        mpatches.Patch(facecolor='#FFD93D', edgecolor='black', label='Solar Canopy Sites (Optimized)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Optimized network topology saved to: {save_path}")
    
    return fig


def plot_optimized_scenario_comparison(save_path='visualizations/optimized_scenario_comparison.png'):
    """
    Compare scenarios with optimized parameters.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    # Optimized parameters
    ppa_rate = get_optimized_ppa_rate()
    net_capex = get_optimized_capex()
    revenue_streams = get_optimized_revenue_streams()
    annual_opex = OPTIMIZED_CONFIG['annual_opex_usd']
    
    # Scenario definitions with optimized parameters
    scenarios = {
        'S0: Baseline': {
            'revenue': 0,
            'capex': 0,
            'description': 'No canopies, grid only'
        },
        'S1: BTM PPA': {
            'revenue': revenue_streams['base_ppa'],
            'capex': net_capex,
            'description': f'PPA at {ppa_rate:.2f}c/kWh'
        },
        'S2: Hybrid': {
            'revenue': revenue_streams['base_ppa'] + revenue_streams['grid_services'] * 0.3,
            'capex': net_capex,
            'description': f'PPA + grid sales'
        },
        'S3: VPP': {
            'revenue': revenue_streams['base_ppa'] + revenue_streams['grid_services'] * 0.5,
            'capex': net_capex,
            'description': 'VPP with grid services'
        },
        'S4: Marketplace': {
            'revenue': revenue_streams['total'],
            'capex': net_capex,
            'description': 'All revenue streams'
        }
    }
    
    scenario_names = list(scenarios.keys())
    revenues = [s['revenue']/1e3 for s in scenarios.values()]
    
    # Calculate financial metrics for each scenario
    irr_values = []
    payback_values = []
    npv_values = []
    
    for scenario_name, scenario_data in scenarios.items():
        if scenario_name == 'S0: Baseline':
            irr_values.append(0)
            payback_values.append(0)
            npv_values.append(0)
        else:
            metrics = calculate_financial_metrics(
                scenario_data['revenue'], annual_opex, scenario_data['capex'],
                25, 0.08
            )
            irr_values.append(metrics['irr'] * 100)
            payback_values.append(metrics['payback_years'])
            npv_values.append(metrics['npv'] / 1e6)
    
    # 1. Revenue Comparison
    ax1 = fig.add_subplot(gs[0, 0])
    
    colors = ['#95A5A6', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD93D']
    bars = ax1.bar(scenario_names, revenues, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Annual Revenue ($1000s)', fontsize=12, fontweight='bold')
    ax1.set_title('Annual Revenue by Scenario (Optimized)', fontsize=13, fontweight='bold')
    ax1.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, revenues):
        if val > 0:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${val:.0f}k', ha='center', va='bottom',
                    fontsize=10, fontweight='bold')
    
    # 2. IRR Comparison
    ax2 = fig.add_subplot(gs[0, 1])
    
    bars = ax2.bar(scenario_names, irr_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax2.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax2.set_ylabel('IRR (%)', fontsize=12, fontweight='bold')
    ax2.set_title('IRR by Scenario (Optimized)', fontsize=13, fontweight='bold')
    ax2.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, irr_values):
        if val > 0:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}%', ha='center', va='bottom',
                    fontsize=10, fontweight='bold')
    
    # 3. Payback Comparison
    ax3 = fig.add_subplot(gs[0, 2])
    
    bars = ax3.bar(scenario_names, payback_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Payback Period (years)', fontsize=12, fontweight='bold')
    ax3.set_title('Payback Period by Scenario (Optimized)', fontsize=13, fontweight='bold')
    ax3.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, payback_values):
        if val > 0:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}y', ha='center', va='bottom',
                    fontsize=10, fontweight='bold')
    
    # 4. NPV Comparison
    ax4 = fig.add_subplot(gs[1, 0])
    
    bars = ax4.bar(scenario_names, npv_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax4.axhline(y=0, color='k', linestyle='--', linewidth=1)
    ax4.set_ylabel('NPV ($M)', fontsize=12, fontweight='bold')
    ax4.set_title('NPV by Scenario (Optimized)', fontsize=13, fontweight='bold')
    ax4.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, npv_values):
        if val != 0:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'${val:.2f}M', ha='center', va='bottom' if val >= 0 else 'top',
                    fontsize=10, fontweight='bold')
    
    # 5. Revenue Streams Breakdown (S4)
    ax5 = fig.add_subplot(gs[1, 1])
    
    rev_sources = ['Base PPA', 'Platform\nFees', 'Grid\nServices', 'EV\nCharging', 'REC\nSales', 'Digital Twin\nLicensing']
    rev_values = [
        revenue_streams['base_ppa']/1e3,
        revenue_streams['platform_fees']/1e3,
        revenue_streams['grid_services']/1e3,
        revenue_streams['ev_charging']/1e3,
        revenue_streams['rec_sales']/1e3,
        revenue_streams.get('digital_twin_licensing', 0)/1e3
    ]
    
    colors_rev = ['#4ECDC4', '#FFD700', '#45B7D1', '#FFA07A', '#98D8C8', '#9B59B6']
    bars = ax5.bar(rev_sources, rev_values, color=colors_rev, alpha=0.8,
                  edgecolor='black', linewidth=1.5)
    ax5.set_ylabel('Revenue ($1000s)', fontsize=12, fontweight='bold')
    ax5.set_title('S4: Revenue Streams Breakdown', fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, rev_values):
        if val > 0:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'${val:.0f}k', ha='center', va='bottom',
                    fontsize=9, fontweight='bold')
    
    # 6. Optimization Impact Summary
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    summary_text = f"""
    OPTIMIZATION IMPACT
    {'='*50}
    
    PPA Rate: {ppa_rate:.2f}c/kWh
    (Market-competitive, -16% from original)
    
    Net CAPEX: ${net_capex/1e6:.2f}M
    (-63% reduction from original)
    
    Battery: 50% power, 0.5h duration
    (Right-sized for cost efficiency)
    
    Total Revenue: ${revenue_streams['total']/1e3:.0f}k/year
    (Multiple revenue streams)
    
    Best Scenario (S4):
        IRR: {irr_values[-1]:.1f}%
        Payback: {payback_values[-1]:.1f} years
        NPV: ${npv_values[-1]:.2f}M
    """
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    # 7-9. Scenario details
    for i, (scenario_name, scenario_data) in enumerate(list(scenarios.items())[:3]):
        ax = fig.add_subplot(gs[2, i])
        ax.axis('off')
        
        if scenario_name == 'S0: Baseline':
            text = f"{scenario_name}\n{scenario_data['description']}\n\nNo investment\nNo revenue"
        else:
            idx = list(scenarios.keys()).index(scenario_name)
            text = f"""{scenario_name}
{scenario_data['description']}

Revenue: ${scenario_data['revenue']/1e3:.0f}k/year
CAPEX: ${scenario_data['capex']/1e6:.2f}M

IRR: {irr_values[idx]:.1f}%
Payback: {payback_values[idx]:.1f} years
NPV: ${npv_values[idx]:.2f}M"""
        
        ax.text(0.5, 0.5, text, transform=ax.transAxes,
               ha='center', va='center', fontsize=10,
               bbox=dict(boxstyle='round,pad=1', facecolor=colors[i], alpha=0.3))
    
    plt.suptitle('Optimized Scenario Comparison\n' + 
                'All Scenarios Using Optimized Parameters (PPA: 7.54c/kWh, CAPEX: $1.81M)',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Optimized scenario comparison saved to: {save_path}")
    
    return fig


def create_all_optimized_visualizations():
    """
    Create all optimized visualizations.
    """
    print("="*80)
    print("CREATING OPTIMIZED VISUALIZATIONS")
    print("="*80)
    
    # 1. Financial comparison
    print("\n1. Financial Comparison...")
    plot_optimized_financial_comparison()
    
    # 2. Network topology
    print("\n2. Network Topology...")
    plot_optimized_network_topology()
    
    # 3. Scenario comparison
    print("\n3. Scenario Comparison...")
    plot_optimized_scenario_comparison()
    
    print("\n" + "="*80)
    print("ALL OPTIMIZED VISUALIZATIONS CREATED!")
    print("="*80)
    print("\nGenerated files:")
    print("  [CHART] visualizations/optimized_financial_comparison.png")
    print("  [CHART] visualizations/optimized_network_topology.png")
    print("  [CHART] visualizations/optimized_scenario_comparison.png")


if __name__ == "__main__":
    create_all_optimized_visualizations()

