"""
Urban DER Exchange - PyPSA Model with NREL PVWatts Data
========================================================

This version uses NREL's PVWatts API to get real solar generation estimates.

Usage:
    $env:NREL_API_KEY="your_key_here"
    python urban_der_exchange_with_pvwatts.py
"""

from urban_der_exchange import (
    create_der_exchange_network,
    calculate_exchange_price,
    print_detailed_report,
    create_visualizations,
    generate_load_profile
)

from nrel_pvwatts_fetcher import get_pvwatts_profiles_for_sites
import pandas as pd
import numpy as np
import os


def simulate_with_pvwatts(api_key, month=6):
    """
    Simulate DER Exchange using NREL PVWatts data.
    """
    print("="*80)
    print("URBAN DER EXCHANGE - WITH NREL PVWATTS DATA")
    print("="*80)
    
    # Define site capacities
    site_capacities = {
        'Site_A': 550,  # South Congress Retail Center
        'Site_B': 380,  # UT Campus Parking Garage
        'Site_C': 800   # Airport Economy Parking
    }
    
    # Fetch PVWatts profiles
    pv_profiles = get_pvwatts_profiles_for_sites(api_key, site_capacities, month)
    
    if pv_profiles is None:
        print("\nERROR: Failed to fetch PVWatts data")
        return None
    
    # Create network
    n = create_der_exchange_network()
    
    # Load profiles
    food_court_load = generate_load_profile(50, 2.0, 11, 14, 'commercial')
    dormitory_load = generate_load_profile(200, 1.5, 14, 18, 'campus')
    cafe_load = generate_load_profile(30, 2.5, 17, 20, 'commercial')
    residential_load = generate_load_profile(400, 1.8, 18, 22, 'residential')
    
    # Set profiles
    for i, snapshot in enumerate(n.snapshots):
        hour = snapshot.hour
        
        # Set generation from PVWatts
        n.generators_t.p_max_pu.loc[snapshot, "Site_A_Solar"] = pv_profiles['Site_A'].iloc[hour] / 550
        n.generators_t.p_max_pu.loc[snapshot, "Site_B_Solar"] = pv_profiles['Site_B'].iloc[hour] / 380
        n.generators_t.p_max_pu.loc[snapshot, "Site_C_Solar"] = pv_profiles['Site_C'].iloc[hour] / 800
        
        # Set loads
        n.loads_t.p_set.loc[snapshot, "FoodCourt_Load"] = food_court_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Dormitory_Load"] = dormitory_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Cafe_Load"] = cafe_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Residential_Load"] = residential_load.iloc[hour]
    
    print("\nCalculating energy flows with REAL PVWatts data...")
    
    # Calculate results
    results = {
        'network': n,
        'generation': {},
        'loads': {},
        'trades': {},
        'revenues': {},
        'exchange_prices': {},
        'data_source': 'NREL PVWatts API'
    }
    
    # Extract generation
    results['generation']['Site_A'] = pv_profiles['Site_A'].values
    results['generation']['Site_B'] = pv_profiles['Site_B'].values
    results['generation']['Site_C'] = pv_profiles['Site_C'].values
    
    # Extract loads
    results['loads']['FoodCourt'] = n.loads_t.p_set.loc[:, 'FoodCourt_Load'].values
    results['loads']['Dormitory'] = n.loads_t.p_set.loc[:, 'Dormitory_Load'].values
    results['loads']['Cafe'] = n.loads_t.p_set.loc[:, 'Cafe_Load'].values
    results['loads']['Residential'] = n.loads_t.p_set.loc[:, 'Residential_Load'].values
    
    # Calculate supply/demand/prices
    total_supply = np.zeros(24)
    total_demand = np.zeros(24)
    exchange_prices = np.zeros(24)
    
    for i in range(24):
        total_supply[i] = (results['generation']['Site_A'][i] + 
                          results['generation']['Site_B'][i] + 
                          results['generation']['Site_C'][i])
        total_demand[i] = (results['loads']['FoodCourt'][i] + 
                          results['loads']['Dormitory'][i] + 
                          results['loads']['Cafe'][i] + 
                          results['loads']['Residential'][i])
        exchange_prices[i] = calculate_exchange_price(total_supply[i], total_demand[i])
    
    results['total_supply'] = total_supply
    results['total_demand'] = total_demand
    results['exchange_prices'] = exchange_prices
    
    # Calculate trades
    hour_1130, hour_1500, hour_1830, hour_2100 = 11, 15, 18, 21
    
    results['trades'] = {
        '1130_FoodCourt': {
            'buyer': 'FoodCourt',
            'energy_kwh': 500,
            'price_cents': exchange_prices[hour_1130],
            'cost_usd': 500 * exchange_prices[hour_1130] / 100,
            'hour': hour_1130
        },
        '1500_Dormitory': {
            'buyer': 'Dormitory',
            'energy_kwh': 1000,
            'price_cents': exchange_prices[hour_1500],
            'cost_usd': 1000 * exchange_prices[hour_1500] / 100,
            'hour': hour_1500
        },
        '1830_Cafe': {
            'buyer': 'Cafe',
            'energy_kwh': 300,
            'price_cents': exchange_prices[hour_1830],
            'cost_usd': 300 * exchange_prices[hour_1830] / 100,
            'hour': hour_1830
        },
        '2100_Residential': {
            'buyer': 'Residential',
            'energy_kwh': 2000,
            'price_cents': exchange_prices[hour_2100],
            'cost_usd': 2000 * exchange_prices[hour_2100] / 100,
            'hour': hour_2100
        }
    }
    
    # Calculate revenues
    total_energy_sold = sum([t['energy_kwh'] for t in results['trades'].values()])
    energy_revenue = sum([t['cost_usd'] for t in results['trades'].values()])
    exchange_fee_revenue = total_energy_sold * 1.5 / 100
    
    results['revenues'] = {
        'total_energy_sold_kwh': total_energy_sold,
        'energy_sale_revenue_usd': energy_revenue,
        'exchange_fee_revenue_usd': exchange_fee_revenue,
        'total_revenue_usd': energy_revenue + exchange_fee_revenue
    }
    
    return results


if __name__ == "__main__":
    # Get API key
    api_key = os.environ.get('NREL_API_KEY', None)
    
    if not api_key:
        print("\nERROR: NREL_API_KEY environment variable not set")
        print("\nPlease set it first:")
        print('  PowerShell: $env:NREL_API_KEY="your_key_here"')
        print('  CMD: set NREL_API_KEY=your_key_here')
        print('  Or use DEMO_KEY for testing: $env:NREL_API_KEY="DEMO_KEY"')
        exit(1)
    
    # Run simulation
    results = simulate_with_pvwatts(api_key, month=6)
    
    if results:
        print("\n" + "="*80)
        print("RESULTS - USING REAL NREL PVWATTS DATA")
        print("="*80)
        print_detailed_report(results)
        
        # Create visualizations
        print("\nGenerating visualizations...")
        create_visualizations(results)
        
        print("\n[SUCCESS] Simulation complete with REAL NREL PVWatts data!")
        print("   - Data source: NREL PVWatts API v8")
        print("   - Location: Austin, TX (30.27°N, 97.74°W)")
        print("   - System specs: Fixed-tilt, 20°, south-facing, 14% losses")
        print("   - Visualization saved as 'der_exchange_analysis.png'")
    else:
        print("\nSimulation failed. Check API key and network connection.")

