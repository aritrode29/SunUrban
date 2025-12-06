"""
Urban DER Exchange - PyPSA Model with NREL Data
================================================

This script uses REAL solar data from NREL's NSRDB instead of synthetic profiles.

Usage:
    python urban_der_exchange_with_nrel.py

Requirements:
    - NREL API key (free): https://developer.nrel.gov/signup/
    - Set environment variable: NREL_API_KEY=your_key_here
    - Or use 'DEMO_KEY' (limited to 30 requests/hour)
"""

# Import the original simulation functions
from urban_der_exchange import (
    create_der_exchange_network,
    calculate_exchange_price,
    print_detailed_report,
    create_visualizations,
    generate_load_profile
)

# Import NREL data fetcher
from nrel_data_fetcher import (
    fetch_nrel_solar_data,
    load_cached_nrel_data,
    generate_pv_profiles_from_nrel
)

import pandas as pd
import numpy as np


def simulate_der_exchange_day_with_nrel_data(use_cached=True, year=2021, month=6):
    """
    Simulate DER Exchange using real NREL solar data.
    
    Parameters:
    -----------
    use_cached : bool
        Try to use cached data first (faster)
    year : int
        Year of data (2000-2021 available)
    month : int
        Month to simulate (1-12)
    
    Returns:
    --------
    dict
        Results dictionary
    """
    print("="*80)
    print("URBAN DER EXCHANGE - SIMULATION WITH REAL NREL DATA")
    print("="*80)
    
    # Step 1: Get NREL solar data
    nrel_data = None
    
    if use_cached:
        nrel_data = load_cached_nrel_data(year)
    
    if nrel_data is None:
        print("\nFetching data from NREL API...")
        nrel_data = fetch_nrel_solar_data(year=year)
        
        if nrel_data is None:
            print("\nERROR: Could not fetch NREL data.")
            print("Falling back to synthetic data...")
            print("To use real data:")
            print("  1. Get API key: https://developer.nrel.gov/signup/")
            print("  2. Set NREL_API_KEY environment variable")
            print("  3. Or enter key when prompted")
            return None
    
    # Step 2: Generate PV profiles from NREL data
    site_capacities = {
        'Site_A': 550,  # South Congress Retail Center
        'Site_B': 380,  # UT Campus Parking Garage
        'Site_C': 800   # Airport Economy Parking
    }
    
    pv_profiles = generate_pv_profiles_from_nrel(
        nrel_data,
        site_capacities,
        month=month,
        day_type='weekday'
    )
    
    # Step 3: Create network and set profiles
    n = create_der_exchange_network()
    
    # Set solar generation from NREL data
    for i, snapshot in enumerate(n.snapshots):
        hour = snapshot.hour
        
        # Set generation using NREL-derived profiles
        n.generators_t.p_max_pu.loc[snapshot, "Site_A_Solar"] = pv_profiles['Site_A'].iloc[hour] / 550
        n.generators_t.p_max_pu.loc[snapshot, "Site_B_Solar"] = pv_profiles['Site_B'].iloc[hour] / 380
        n.generators_t.p_max_pu.loc[snapshot, "Site_C_Solar"] = pv_profiles['Site_C'].iloc[hour] / 800
        
        # Set loads (same as before)
        food_court_load = generate_load_profile(50, 2.0, 11, 14, 'commercial')
        dormitory_load = generate_load_profile(200, 1.5, 14, 18, 'campus')
        cafe_load = generate_load_profile(30, 2.5, 17, 20, 'commercial')
        residential_load = generate_load_profile(400, 1.8, 18, 22, 'residential')
        
        n.loads_t.p_set.loc[snapshot, "FoodCourt_Load"] = food_court_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Dormitory_Load"] = dormitory_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Cafe_Load"] = cafe_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Residential_Load"] = residential_load.iloc[hour]
    
    print("\nCalculating energy flows (using NREL data)...")
    
    # Step 4: Calculate results (simplified approach)
    results = {
        'network': n,
        'generation': {},
        'loads': {},
        'trades': {},
        'revenues': {},
        'exchange_prices': {},
        'nrel_data': True  # Flag that we used real data
    }
    
    # Extract generation from NREL profiles
    results['generation']['Site_A'] = pv_profiles['Site_A'].values
    results['generation']['Site_B'] = pv_profiles['Site_B'].values
    results['generation']['Site_C'] = pv_profiles['Site_C'].values
    
    # Extract loads
    results['loads']['FoodCourt'] = n.loads_t.p_set.loc[:, 'FoodCourt_Load'].values
    results['loads']['Dormitory'] = n.loads_t.p_set.loc[:, 'Dormitory_Load'].values
    results['loads']['Cafe'] = n.loads_t.p_set.loc[:, 'Cafe_Load'].values
    results['loads']['Residential'] = n.loads_t.p_set.loc[:, 'Residential_Load'].values
    
    # Calculate supply, demand, and prices
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
    
    # Calculate trades (same scenarios as before)
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
    # Run simulation with NREL data
    results = simulate_der_exchange_day_with_nrel_data(
        use_cached=True,
        year=2021,
        month=6  # June (summer)
    )
    
    if results is not None:
        # Print report
        print("\n" + "="*80)
        print("RESULTS (Using Real NREL Solar Data)")
        print("="*80)
        print_detailed_report(results)
        
        # Create visualizations
        print("\nGenerating visualizations...")
        create_visualizations(results)
        
        print("\n[SUCCESS] Simulation complete with REAL NREL data!")
        print("   - Report printed above")
        print("   - Visualization saved as 'der_exchange_analysis.png'")
    else:
        print("\nSimulation could not run with NREL data.")
        print("Run 'python urban_der_exchange.py' to use synthetic data instead.")

