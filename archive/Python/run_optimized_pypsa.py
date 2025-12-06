"""
Run Optimized PyPSA Scenarios
=============================

Main runner for optimized PyPSA scenario analysis with comprehensive outputs.
"""

import sys
sys.path.insert(0, 'pypsa_models')

from run_optimized_pypsa_scenarios import run_all_optimized_scenarios
from plot_optimized_pypsa_outputs import (
    plot_comprehensive_pypsa_outputs,
    plot_load_analysis,
    plot_optimization_details
)

if __name__ == "__main__":
    print("="*80)
    print("OPTIMIZED PYPSA SCENARIO ANALYSIS")
    print("="*80)
    print("\nRunning scenarios with optimized parameters:")
    print("  - Optimized battery sizes (50% power, 0.5h duration)")
    print("  - Optimized PPA rate (7.54¢/kWh)")
    print("  - All revenue streams including Digital Twin")
    
    # Run scenarios
    print("\n" + "="*80)
    print("STEP 1: Running PyPSA Optimizations")
    print("="*80)
    results = run_all_optimized_scenarios()
    
    # Generate visualizations
    print("\n" + "="*80)
    print("STEP 2: Generating Comprehensive Visualizations")
    print("="*80)
    
    print("\n1. Comprehensive PyPSA Outputs...")
    plot_comprehensive_pypsa_outputs(results)
    
    print("\n2. Load Analysis...")
    plot_load_analysis(results)
    
    print("\n3. Optimization Details...")
    plot_optimization_details(results)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated visualizations:")
    print("  - visualizations/optimized_pypsa_comprehensive.png")
    print("  - visualizations/optimized_pypsa_loads.png")
    print("  - visualizations/optimized_pypsa_optimization.png")
    print("\nThese files contain:")
    print("  - Generation and load profiles")
    print("  - Battery operation (charge/discharge/SOC)")
    print("  - Grid interaction")
    print("  - Revenue and cost breakdowns")
    print("  - Optimization metrics")
    print("  - Energy flow analysis")
    print("\n" + "="*80)

