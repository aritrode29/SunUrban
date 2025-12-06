"""
Quick Start Example - Urban DER Exchange
========================================

This script demonstrates how to use the Urban DER Exchange PyPSA model
with custom parameters.
"""

from urban_der_exchange import (
    create_der_exchange_network,
    generate_solar_profile,
    generate_load_profile,
    calculate_exchange_price,
    simulate_der_exchange_day,
    print_detailed_report,
    create_visualizations
)

# Example 1: Run the default scenario
print("Running default scenario...")
results = simulate_der_exchange_day()
print_detailed_report(results)

# Example 2: Customize a site's generation profile
print("\n" + "="*80)
print("CUSTOM SCENARIO: Higher capacity Site A")
print("="*80)

# Modify Site A to have higher capacity
def custom_scenario():
    from pypsa import Network
    import pandas as pd
    import numpy as np
    
    n = create_der_exchange_network()
    
    # Increase Site A capacity to 750 kW (from 550 kW)
    n.generators.loc['Site_A_Solar', 'p_nom'] = 750
    n.links.loc['Site_A_to_Exchange', 'p_nom'] = 750
    n.links.loc['Site_A_Charge', 'p_nom'] = 750
    n.links.loc['Site_A_Discharge', 'p_nom'] = 750
    n.stores.loc['Site_A_Battery', 'e_nom'] = 1500  # 2 hours @ 750 kW
    
    # Generate profiles with new capacity
    site_a_gen = generate_solar_profile(750, 11, 16, base_irradiance=0.85)
    site_b_gen = generate_solar_profile(380, 14, 19, base_irradiance=0.80)
    site_c_gen = generate_solar_profile(800, 12, 20, base_irradiance=0.82)
    
    # Load profiles (same as default)
    food_court_load = generate_load_profile(50, 2.0, 11, 14, 'commercial')
    dormitory_load = generate_load_profile(200, 1.5, 14, 18, 'campus')
    cafe_load = generate_load_profile(30, 2.5, 17, 20, 'commercial')
    residential_load = generate_load_profile(400, 1.8, 18, 22, 'residential')
    
    # Set time-varying profiles
    for i, snapshot in enumerate(n.snapshots):
        hour = snapshot.hour
        n.generators_t.p_max_pu.loc[snapshot, "Site_A_Solar"] = site_a_gen.iloc[hour] / 750
        n.generators_t.p_max_pu.loc[snapshot, "Site_B_Solar"] = site_b_gen.iloc[hour] / 380
        n.generators_t.p_max_pu.loc[snapshot, "Site_C_Solar"] = site_c_gen.iloc[hour] / 800
        
        n.loads_t.p_set.loc[snapshot, "FoodCourt_Load"] = food_court_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Dormitory_Load"] = dormitory_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Cafe_Load"] = cafe_load.iloc[hour]
        n.loads_t.p_set.loc[snapshot, "Residential_Load"] = residential_load.iloc[hour]
    
    # Optimize
    print("Optimizing network...")
    n.optimize(solver_name='glpk')
    
    # Calculate results (simplified - same structure as main function)
    results = {
        'generation': {
            'Site_A': n.generators_t.p.loc[:, 'Site_A_Solar'].values,
            'Site_B': n.generators_t.p.loc[:, 'Site_B_Solar'].values,
            'Site_C': n.generators_t.p.loc[:, 'Site_C_Solar'].values
        },
        'loads': {
            'FoodCourt': n.loads_t.p.loc[:, 'FoodCourt_Load'].values,
            'Dormitory': n.loads_t.p.loc[:, 'Dormitory_Load'].values,
            'Cafe': n.loads_t.p.loc[:, 'Cafe_Load'].values,
            'Residential': n.loads_t.p.loc[:, 'Residential_Load'].values
        },
        'total_supply': np.zeros(24),
        'total_demand': np.zeros(24),
        'exchange_prices': np.zeros(24),
        'trades': {},
        'revenues': {}
    }
    
    # Calculate supply, demand, prices
    for i in range(24):
        results['total_supply'][i] = (results['generation']['Site_A'][i] + 
                                     results['generation']['Site_B'][i] + 
                                     results['generation']['Site_C'][i])
        results['total_demand'][i] = (results['loads']['FoodCourt'][i] + 
                                     results['loads']['Dormitory'][i] + 
                                     results['loads']['Cafe'][i] + 
                                     results['loads']['Residential'][i])
        results['exchange_prices'][i] = calculate_exchange_price(
            results['total_supply'][i], 
            results['total_demand'][i]
        )
    
    # Same trades as default
    hour_1130, hour_1500, hour_1830, hour_2100 = 11, 15, 18, 21
    results['trades'] = {
        '1130_FoodCourt': {
            'buyer': 'FoodCourt',
            'energy_kwh': 500,
            'price_cents': results['exchange_prices'][hour_1130],
            'cost_usd': 500 * results['exchange_prices'][hour_1130] / 100,
            'hour': hour_1130
        },
        '1500_Dormitory': {
            'buyer': 'Dormitory',
            'energy_kwh': 1000,
            'price_cents': results['exchange_prices'][hour_1500],
            'cost_usd': 1000 * results['exchange_prices'][hour_1500] / 100,
            'hour': hour_1500
        },
        '1830_Cafe': {
            'buyer': 'Cafe',
            'energy_kwh': 300,
            'price_cents': results['exchange_prices'][hour_1830],
            'cost_usd': 300 * results['exchange_prices'][hour_1830] / 100,
            'hour': hour_1830
        },
        '2100_Residential': {
            'buyer': 'Residential',
            'energy_kwh': 2000,
            'price_cents': results['exchange_prices'][hour_2100],
            'cost_usd': 2000 * results['exchange_prices'][hour_2100] / 100,
            'hour': hour_2100
        }
    }
    
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

# Run custom scenario
custom_results = custom_scenario()
print_detailed_report(custom_results)

print("\n✅ Examples complete!")

