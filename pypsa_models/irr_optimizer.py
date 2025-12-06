"""
IRR Optimizer
=============

Optimizes PPA rate, CAPEX, battery sizing, and revenue streams to achieve target IRR
while maintaining market competitiveness.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, differential_evolution
from capex_analysis import calculate_financial_metrics, calculate_site_capex, COST_ASSUMPTIONS
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


class IRROptimizer:
    """
    Optimizer for finding optimal configurations to achieve target IRR.
    """
    
    def __init__(self, target_irr=0.10, project_lifetime=25, discount_rate=0.08):
        """
        Initialize optimizer.
        
        Parameters:
        -----------
        target_irr : float
            Target IRR (default 10%)
        project_lifetime : int
            Project lifetime in years
        discount_rate : float
            Discount rate for NPV
        """
        self.target_irr = target_irr
        self.project_lifetime = project_lifetime
        self.discount_rate = discount_rate
        
        # Base assumptions
        self.base_solar_kw = 1730  # Total for 3 sites
        self.base_battery_kw = 1730
        self.base_battery_kwh = 3460
        self.base_annual_generation_mwh = 3219  # MWh/year
        self.base_opex_per_kw = 25  # $/kW/year
        
    def calculate_irr_from_params(self, ppa_rate, net_capex, annual_opex, 
                                  annual_generation_mwh=None):
        """
        Calculate IRR from parameters.
        
        Parameters:
        -----------
        ppa_rate : float
            PPA rate in cents/kWh
        net_capex : float
            Net CAPEX in USD
        annual_opex : float
            Annual OPEX in USD
        annual_generation_mwh : float, optional
            Annual generation (default: self.base_annual_generation_mwh)
        
        Returns:
        --------
        float
            IRR as decimal (e.g., 0.10 for 10%)
        """
        if annual_generation_mwh is None:
            annual_generation_mwh = self.base_annual_generation_mwh
        
        annual_revenue = ppa_rate * 10 * annual_generation_mwh  # Convert to $/year
        
        metrics = calculate_financial_metrics(
            annual_revenue, annual_opex, net_capex,
            self.project_lifetime, self.discount_rate
        )
        
        return metrics['irr']
    
    def optimize_ppa_and_capex(self, market_ppa_min=7.0, market_ppa_max=8.0,
                               capex_min_mult=0.3, capex_max_mult=1.0):
        """
        Optimize PPA rate and CAPEX to achieve target IRR.
        
        Parameters:
        -----------
        market_ppa_min : float
            Minimum market-competitive PPA rate (cents/kWh)
        market_ppa_max : float
            Maximum market-competitive PPA rate (cents/kWh)
        capex_min_mult : float
            Minimum CAPEX as multiplier of base
        capex_max_mult : float
            Maximum CAPEX as multiplier of base
        
        Returns:
        --------
        dict
            Optimal solution
        """
        base_capex = 4860000  # Current net CAPEX
        base_opex = 43000
        
        def objective(x):
            """
            Objective: minimize distance from target IRR.
            x[0] = PPA rate (cents/kWh)
            x[1] = CAPEX multiplier
            """
            ppa_rate = x[0]
            capex_mult = x[1]
            net_capex = base_capex * capex_mult
            
            irr = self.calculate_irr_from_params(ppa_rate, net_capex, base_opex)
            
            # Penalty for being away from target
            irr_error = abs(irr - self.target_irr)
            
            # Also prefer lower CAPEX (cost minimization)
            capex_penalty = capex_mult * 0.01  # Small penalty for higher CAPEX
            
            return irr_error + capex_penalty
        
        # Constraints
        constraints = [
            {'type': 'ineq', 'fun': lambda x: x[0] - market_ppa_min},  # PPA >= min
            {'type': 'ineq', 'fun': lambda x: market_ppa_max - x[0]},  # PPA <= max
            {'type': 'ineq', 'fun': lambda x: x[1] - capex_min_mult},  # CAPEX >= min
            {'type': 'ineq', 'fun': lambda x: capex_max_mult - x[1]},  # CAPEX <= max
        ]
        
        # Bounds
        bounds = [(market_ppa_min, market_ppa_max), (capex_min_mult, capex_max_mult)]
        
        # Initial guess
        x0 = [7.5, 0.5]  # 7.5¢ PPA, 50% of base CAPEX
        
        # Optimize
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, 
                         constraints=constraints, options={'maxiter': 1000})
        
        optimal_ppa = result.x[0]
        optimal_capex_mult = result.x[1]
        optimal_capex = base_capex * optimal_capex_mult
        
        # Calculate final metrics
        annual_revenue = optimal_ppa * 10 * self.base_annual_generation_mwh
        final_metrics = calculate_financial_metrics(
            annual_revenue, base_opex, optimal_capex,
            self.project_lifetime, self.discount_rate
        )
        
        solution = {
            'ppa_rate': optimal_ppa,
            'net_capex': optimal_capex,
            'capex_reduction_pct': (1 - optimal_capex_mult) * 100,
            'annual_revenue': annual_revenue,
            'annual_opex': base_opex,
            'irr': final_metrics['irr'],
            'payback_years': final_metrics['payback_years'],
            'npv': final_metrics['npv'],
            'annual_cash_flow': final_metrics['annual_cash_flow'],
            'success': result.success
        }
        
        return solution
    
    def optimize_battery_sizing(self, ppa_rate=7.5, target_capex=None):
        """
        Optimize battery sizing (power and duration) for given PPA rate and CAPEX target.
        
        Parameters:
        -----------
        ppa_rate : float
            PPA rate in cents/kWh
        target_capex : float, optional
            Target net CAPEX (if None, will optimize)
        
        Returns:
        --------
        dict
            Optimal battery configuration
        """
        base_solar_kw = 1730
        base_opex = 43000
        
        # If target_capex is provided, use it directly
        if target_capex:
            # Find battery configuration that fits within target CAPEX
            # We'll scale battery costs proportionally
            base_site_capex = calculate_site_capex(base_solar_kw, base_solar_kw, base_solar_kw * 2.0)
            base_net_capex = base_site_capex['net_capex']
            capex_scale = target_capex / base_net_capex
            
            # Battery sizing options
            battery_durations = [0.5, 1.0, 1.5, 2.0]  # hours
            battery_power_fractions = [0.5, 0.75, 1.0]  # fraction of solar capacity
            
            best_solution = None
            best_irr = -1
            
            for duration in battery_durations:
                for power_frac in battery_power_fractions:
                    battery_kw = base_solar_kw * power_frac
                    battery_kwh = battery_kw * duration
                    
                    # Estimate CAPEX with scaling
                    # Battery is ~40% of CAPEX, so scale it
                    battery_cost_per_kwh = COST_ASSUMPTIONS['battery_storage']['cost_per_kwh']
                    battery_cost_per_kw = COST_ASSUMPTIONS['battery_storage']['cost_per_kw']
                    battery_cost = (battery_kw * battery_cost_per_kw + 
                                  battery_kwh * battery_cost_per_kwh) * capex_scale
                    
                    # Other costs scale proportionally
                    other_costs = (base_net_capex - base_site_capex['battery_total']) * capex_scale
                    estimated_net_capex = battery_cost + other_costs
                    
                    # Calculate IRR
                    annual_revenue = ppa_rate * 10 * self.base_annual_generation_mwh
                    annual_opex = base_solar_kw * self.base_opex_per_kw
                    
                    metrics = calculate_financial_metrics(
                        annual_revenue, annual_opex, estimated_net_capex,
                        self.project_lifetime, self.discount_rate
                    )
                    
                    if metrics['irr'] > best_irr:
                        best_irr = metrics['irr']
                        best_solution = {
                            'battery_kw': battery_kw,
                            'battery_kwh': battery_kwh,
                            'duration_hours': duration,
                            'power_fraction': power_frac,
                            'net_capex': estimated_net_capex,
                            'irr': metrics['irr'],
                            'payback_years': metrics['payback_years'],
                            'npv': metrics['npv'],
                            'battery_cost': battery_cost
                        }
        else:
            # No target CAPEX, optimize normally
            battery_durations = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
            battery_power_fractions = [0.5, 0.75, 1.0, 1.25]
            
            best_solution = None
            best_irr = -1
            
            for duration in battery_durations:
                for power_frac in battery_power_fractions:
                    battery_kw = base_solar_kw * power_frac
                    battery_kwh = battery_kw * duration
                    
                    site_capex = calculate_site_capex(base_solar_kw, battery_kw, battery_kwh)
                    net_capex = site_capex['net_capex']
                    
                    annual_revenue = ppa_rate * 10 * self.base_annual_generation_mwh
                    annual_opex = base_solar_kw * self.base_opex_per_kw
                    
                    metrics = calculate_financial_metrics(
                        annual_revenue, annual_opex, net_capex,
                        self.project_lifetime, self.discount_rate
                    )
                    
                    if metrics['irr'] > best_irr:
                        best_irr = metrics['irr']
                        best_solution = {
                            'battery_kw': battery_kw,
                            'battery_kwh': battery_kwh,
                            'duration_hours': duration,
                            'power_fraction': power_frac,
                            'net_capex': net_capex,
                            'irr': metrics['irr'],
                            'payback_years': metrics['payback_years'],
                            'npv': metrics['npv'],
                            'battery_cost': site_capex['battery_total']
                        }
        
        # If no solution found, return default using target CAPEX
        if best_solution is None:
            if target_capex:
                net_capex = target_capex
            else:
                site_capex = calculate_site_capex(base_solar_kw, base_solar_kw, base_solar_kw * 2.0)
                net_capex = site_capex['net_capex']
            
            annual_revenue = ppa_rate * 10 * self.base_annual_generation_mwh
            annual_opex = base_solar_kw * self.base_opex_per_kw
            metrics = calculate_financial_metrics(
                annual_revenue, annual_opex, net_capex,
                self.project_lifetime, self.discount_rate
            )
            best_solution = {
                'battery_kw': base_solar_kw,
                'battery_kwh': base_solar_kw * 1.5,
                'duration_hours': 1.5,
                'power_fraction': 1.0,
                'net_capex': net_capex,
                'irr': metrics['irr'],
                'payback_years': metrics['payback_years'],
                'npv': metrics['npv'],
                'battery_cost': net_capex * 0.4  # Estimate
            }
        
        return best_solution
    
    def optimize_with_revenue_streams(self, base_ppa=7.5, target_capex=2500000, 
                                     include_platform_fees=True):
        """
        Optimize with multiple revenue streams.
        
        Parameters:
        -----------
        base_ppa : float
            Base PPA rate
        target_capex : float
            Target net CAPEX
        include_platform_fees : bool
            Whether to include platform/exchange fees (1.5¢/kWh on marketplace trades)
        
        Returns:
        --------
        dict
            Optimal configuration with revenue streams
        """
        base_opex = 43000
        base_revenue = base_ppa * 10 * self.base_annual_generation_mwh
        
        # Platform fees: 1.5¢/kWh on marketplace trades
        # Estimate: 30-50% of generation goes through marketplace
        if include_platform_fees:
            marketplace_fraction = 0.4  # 40% of generation traded on marketplace
            platform_fee_rate = 1.5  # cents/kWh
            platform_fee_revenue = (marketplace_fraction * self.base_annual_generation_mwh * 
                                  platform_fee_rate * 10)  # Convert to $/year
        else:
            platform_fee_revenue = 0
        
        # Revenue stream options
        grid_services_options = [0, 25000, 50000, 75000, 100000]  # $/year
        ev_charging_options = [0, 10000, 20000, 30000, 50000]  # $/year
        rec_sales_options = [0, 10000, 20000, 30000]  # $/year
        digital_twin_options = [0, 25000, 50000, 75000, 100000]  # $/year (data licensing SaaS)
        
        best_solution = None
        best_irr = -1
        
        for grid_services in grid_services_options:
            for ev_charging in ev_charging_options:
                for rec_sales in rec_sales_options:
                    for digital_twin in digital_twin_options:
                        total_revenue = (base_revenue + grid_services + ev_charging + 
                                       rec_sales + platform_fee_revenue + digital_twin)
                    
                    metrics = calculate_financial_metrics(
                        total_revenue, base_opex, target_capex,
                        self.project_lifetime, self.discount_rate
                    )
                    
                    if metrics['irr'] > best_irr:
                        best_irr = metrics['irr']
                        best_solution = {
                            'base_ppa': base_ppa,
                            'base_revenue': base_revenue,
                            'platform_fees': platform_fee_revenue,
                            'grid_services': grid_services,
                            'ev_charging': ev_charging,
                            'rec_sales': rec_sales,
                            'digital_twin_licensing': digital_twin,
                            'total_revenue': total_revenue,
                            'net_capex': target_capex,
                            'irr': metrics['irr'],
                            'payback_years': metrics['payback_years'],
                            'npv': metrics['npv']
                        }
        
        return best_solution
    
    def comprehensive_optimization(self):
        """
        Comprehensive optimization across all parameters.
        
        Returns:
        --------
        dict
            Best overall solution
        """
        print("="*80)
        print("COMPREHENSIVE IRR OPTIMIZATION")
        print("="*80)
        
        results = {}
        
        # 1. Optimize PPA and CAPEX
        print("\n1. Optimizing PPA rate and CAPEX...")
        solution_1 = self.optimize_ppa_and_capex()
        results['ppa_capex_optimization'] = solution_1
        
        # 2. Optimize battery sizing
        print("2. Optimizing battery sizing...")
        solution_2 = self.optimize_battery_sizing(
            ppa_rate=solution_1['ppa_rate'],
            target_capex=solution_1['net_capex']
        )
        results['battery_optimization'] = solution_2
        
        # 3. Optimize with revenue streams
        print("3. Optimizing revenue streams...")
        solution_3 = self.optimize_with_revenue_streams(
            base_ppa=solution_1['ppa_rate'],
            target_capex=solution_1['net_capex'],
            include_platform_fees=True  # Include platform fees
        )
        results['revenue_optimization'] = solution_3
        
        # 4. Find best overall
        all_solutions = [
            ('PPA+CAPEX', solution_1),
            ('Battery', solution_2),
            ('Revenue Streams', solution_3)
        ]
        
        # Filter out None solutions
        valid_solutions = [(name, sol) for name, sol in all_solutions if sol is not None]
        
        if valid_solutions:
            best = max(valid_solutions, key=lambda x: x[1]['irr'])
            results['best_solution'] = {
                'strategy': best[0],
                **best[1]
            }
        else:
            # Fallback to solution_1
            results['best_solution'] = {
                'strategy': 'PPA+CAPEX',
                **solution_1
            }
        
        return results


def plot_optimization_results(optimizer_results, save_path='visualizations/irr_optimization_results.png'):
    """
    Visualize optimization results.
    """
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    sol1 = optimizer_results['ppa_capex_optimization']
    sol2 = optimizer_results['battery_optimization']
    sol3 = optimizer_results['revenue_optimization']
    best = optimizer_results['best_solution']
    
    # 1. Optimization Results Comparison
    ax1 = fig.add_subplot(gs[0, 0])
    
    strategies = ['PPA+CAPEX\nOptimization', 'Battery\nOptimization', 
                  'Revenue\nStreams', 'Best\nSolution']
    irr_values = [sol1['irr']*100, sol2['irr']*100, 
                 sol3['irr']*100, best['irr']*100]
    
    colors = ['#4ECDC4', '#45B7D1', '#FFA07A', '#FFD700']
    bars = ax1.bar(strategies, irr_values, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax1.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax1.set_ylabel('IRR (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Optimization Results Comparison', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.9)
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, irr_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    
    # 2. Best Solution Details
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    
    best_text = f"""
    BEST OPTIMIZED SOLUTION
    {'='*40}
    
    Strategy: {best['strategy']}
    
    PPA Rate: {sol1['ppa_rate']:.2f}¢/kWh
    Net CAPEX: ${sol1['net_capex']/1e6:.2f}M
    CAPEX Reduction: -{sol1['capex_reduction_pct']:.0f}%
    
    Annual Revenue: ${sol1['annual_revenue']/1e3:.0f}k
    Annual OPEX: ${sol1['annual_opex']/1e3:.0f}k
    Cash Flow: ${sol1['annual_cash_flow']/1e3:.0f}k
    
    IRR: {best['irr']*100:.1f}%
    Payback: {best['payback_years']:.1f} years
    NPV: ${best['npv']/1e6:.2f}M
    
    Status: {'TARGET MET!' if best['irr'] >= 0.10 else 'Below Target'}
    """
    
    ax2.text(0.1, 0.9, best_text, transform=ax2.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8))
    
    # 3. Battery Optimization Results
    ax3 = fig.add_subplot(gs[0, 2])
    
    if 'battery_kw' in sol2:
        battery_data = {
            'Power (kW)': sol2['battery_kw'],
            'Energy (kWh)': sol2['battery_kwh'],
            'Duration (h)': sol2['duration_hours'],
            'Cost ($M)': sol2['battery_cost']/1e6
        }
        
        x_pos = np.arange(len(battery_data))
        values = list(battery_data.values())
        labels = list(battery_data.keys())
        
        bars = ax3.bar(labels, values, color='#4ECDC4', alpha=0.8,
                      edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Value', fontsize=11, fontweight='bold')
        ax3.set_title('Optimal Battery Configuration', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        for bar, val, label in zip(bars, values, labels):
            height = bar.get_height()
            if 'Cost' in label:
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'${val:.2f}M', ha='center', va='bottom', fontsize=9)
            else:
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{val:.0f}', ha='center', va='bottom', fontsize=9)
    
    # 4. Revenue Streams Breakdown
    ax4 = fig.add_subplot(gs[1, 0])
    
    revenue_sources = ['Base PPA', 'Platform\nFees', 'Grid Services', 'EV Charging', 'REC Sales']
    revenue_values = [
        sol3['base_revenue']/1e3,
        sol3.get('platform_fees', 0)/1e3,
        sol3['grid_services']/1e3,
        sol3['ev_charging']/1e3,
        sol3['rec_sales']/1e3
    ]
    
    colors_rev = ['#4ECDC4', '#FFD700', '#45B7D1', '#FFA07A', '#98D8C8']
    bars = ax4.bar(revenue_sources, revenue_values, color=colors_rev, alpha=0.8,
                  edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('Revenue ($1000s)', fontsize=11, fontweight='bold')
    ax4.set_title('Optimal Revenue Streams (with Platform Fees)', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, revenue_values):
        if val > 0:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'${val:.0f}k', ha='center', va='bottom',
                    fontsize=9, fontweight='bold')
    
    # 5. Parameter Sensitivity
    ax5 = fig.add_subplot(gs[1, 1])
    
    # Test sensitivity of IRR to PPA rate
    ppa_range = np.arange(6.0, 9.5, 0.25)
    irr_sensitivity = []
    
    for ppa in ppa_range:
        irr = optimizer_results['ppa_capex_optimization']['irr']
        # Approximate sensitivity
        base_ppa = optimizer_results['ppa_capex_optimization']['ppa_rate']
        revenue_change = (ppa - base_ppa) / base_ppa
        # Rough approximation: 1% revenue change ≈ 0.5% IRR change
        estimated_irr = irr + (revenue_change * 0.5)
        irr_sensitivity.append(estimated_irr * 100)
    
    ax5.plot(ppa_range, irr_sensitivity, 'o-', linewidth=3, markersize=6,
            color='#4ECDC4', label='IRR Sensitivity')
    ax5.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax5.axvline(x=sol1['ppa_rate'], color='red', linestyle=':', linewidth=2,
               label=f'Optimal ({sol1["ppa_rate"]:.2f}¢)')
    ax5.set_xlabel('PPA Rate (¢/kWh)', fontsize=11, fontweight='bold')
    ax5.set_ylabel('IRR (%)', fontsize=11, fontweight='bold')
    ax5.set_title('IRR Sensitivity to PPA Rate', fontsize=12, fontweight='bold')
    ax5.legend(framealpha=0.9)
    ax5.grid(True, alpha=0.3)
    
    # 6. CAPEX Reduction Breakdown
    ax6 = fig.add_subplot(gs[1, 2])
    
    current_capex = 4860000
    optimal_capex = sol1['net_capex']
    reduction = current_capex - optimal_capex
    
    # Estimate component reductions
    components = ['Battery\nCost', 'Battery\nSizing', 'Scale\nEconomies', 
                 'Standardization', 'Other']
    reductions = [
        reduction * 0.40,  # Battery cost (40% of total)
        reduction * 0.15,  # Battery sizing (15%)
        reduction * 0.25,  # Scale (25%)
        reduction * 0.10,  # Standardization (10%)
        reduction * 0.10   # Other (10%)
    ]
    
    colors_red = ['#FF6B6B', '#FFA07A', '#FFD700', '#98D8C8', '#4ECDC4']
    bars = ax6.bar(components, [r/1e6 for r in reductions], color=colors_red,
                  alpha=0.8, edgecolor='black', linewidth=1.5)
    ax6.set_ylabel('CAPEX Reduction ($M)', fontsize=11, fontweight='bold')
    ax6.set_title('CAPEX Reduction Breakdown', fontsize=12, fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, reductions):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'${val/1e6:.2f}M', ha='center', va='bottom',
                fontsize=9, fontweight='bold')
    
    # 7. Optimization Path
    ax7 = fig.add_subplot(gs[2, 0])
    
    steps = ['Current', 'Optimize\nPPA+CAPEX', 'Optimize\nBattery', 
            'Add Revenue\nStreams', 'Final']
    irr_path = [1.9, sol1['irr']*100, sol2['irr']*100, 
               sol3['irr']*100, best['irr']*100]
    
    ax7.plot(steps, irr_path, 'o-', linewidth=3, markersize=10,
            color='#4ECDC4', label='IRR Path')
    ax7.axhline(y=10, color='green', linestyle='--', linewidth=2, label='10% Target')
    ax7.fill_between(steps, 0, irr_path, alpha=0.3, color='#4ECDC4')
    ax7.set_ylabel('IRR (%)', fontsize=11, fontweight='bold')
    ax7.set_title('Optimization Path to Target IRR', fontsize=12, fontweight='bold')
    ax7.legend(framealpha=0.9)
    ax7.grid(True, alpha=0.3)
    
    for i, (step, irr) in enumerate(zip(steps, irr_path)):
        ax7.text(i, irr, f'{irr:.1f}%', ha='center', va='bottom',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # 8. Implementation Roadmap
    ax8 = fig.add_subplot(gs[2, 1:])
    ax8.axis('off')
    
    roadmap = f"""
    IMPLEMENTATION ROADMAP
    {'='*60}
    
    Phase 1 (2025): Foundation
        - Optimize battery sizing: {sol2.get('duration_hours', 2.0):.1f}h duration
        - Standardize designs
        - Scale to 5-10 sites
        Target: 5-7% IRR
    
    Phase 2 (2026-2027): Cost Reduction
        - Battery costs: $400/kWh → $200/kWh
        - Scale to 10-20 sites
        - Optimize PPA: {sol1['ppa_rate']:.2f}¢/kWh
        Target: 8-10% IRR
    
    Phase 3 (2028+): Revenue Enhancement
        - Add grid services: ${sol3['grid_services']/1e3:.0f}k/year
        - Add EV charging: ${sol3['ev_charging']/1e3:.0f}k/year
        - Add REC sales: ${sol3['rec_sales']/1e3:.0f}k/year
        Target: 10-12% IRR
    
    Final Configuration:
        PPA Rate: {sol1['ppa_rate']:.2f}¢/kWh (market-competitive)
        Net CAPEX: ${sol1['net_capex']/1e6:.2f}M (-{sol1['capex_reduction_pct']:.0f}% reduction)
        Total Revenue: ${sol3['total_revenue']/1e3:.0f}k/year
        IRR: {best['irr']*100:.1f}%
        Payback: {best['payback_years']:.1f} years
    """
    
    ax8.text(0.05, 0.95, roadmap, transform=ax8.transAxes,
            fontsize=9, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    plt.suptitle('IRR Optimization Results\n' + 
                'Optimal Configuration for 10%+ IRR with Market-Competitive PPA',
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Optimization results saved to: {save_path}")
    
    return fig


if __name__ == "__main__":
    optimizer = IRROptimizer(target_irr=0.10)
    
    print("Running comprehensive optimization...")
    results = optimizer.comprehensive_optimization()
    
    print("\n" + "="*80)
    print("OPTIMIZATION RESULTS")
    print("="*80)
    
    best = results['best_solution']
    print(f"\nBest Solution ({best['strategy']}):")
    print(f"  PPA Rate: {results['ppa_capex_optimization']['ppa_rate']:.2f}¢/kWh")
    print(f"  Net CAPEX: ${best['net_capex']/1e6:.2f}M")
    print(f"  Total Revenue: ${results['revenue_optimization']['total_revenue']/1e3:.0f}k/year")
    print(f"  IRR: {best['irr']*100:.1f}%")
    print(f"  Payback: {best['payback_years']:.1f} years")
    print(f"  NPV: ${best['npv']/1e6:.2f}M")
    
    # Create visualization
    plot_optimization_results(results)

