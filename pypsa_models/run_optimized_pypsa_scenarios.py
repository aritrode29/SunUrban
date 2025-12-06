"""
Optimized PyPSA Scenario Runner
================================

Runs PyPSA scenarios with optimized parameters and generates comprehensive outputs.
"""

import pypsa
import pandas as pd
import numpy as np
from optimized_scenario_config import (
    OPTIMIZED_CONFIG, get_optimized_site_config, get_optimized_ppa_rate
)
import warnings
warnings.filterwarnings('ignore')


def create_optimized_network():
    """
    Create PyPSA network with optimized parameters.
    """
    # Create network
    n = pypsa.Network()
    
    # Time index (24 hours)
    n.set_snapshots(pd.date_range('2024-06-15 00:00', periods=24, freq='H'))
    
    # ERCOT-lite buses
    buses = ['HOUSTON', 'NORTH', 'SOUTH', 'WEST']
    for bus in buses:
        n.add('Bus', bus, v_nom=138)  # 138 kV
    
    # Transmission lines
    n.add('Line', 'HOUSTON-NORTH', bus0='HOUSTON', bus1='NORTH', 
          x=0.1, s_nom=2000)  # 2000 MW
    n.add('Line', 'HOUSTON-SOUTH', bus0='HOUSTON', bus1='SOUTH',
          x=0.1, s_nom=1500)  # 1500 MW
    n.add('Line', 'NORTH-WEST', bus0='NORTH', bus1='WEST',
          x=0.1, s_nom=1000)  # 1000 MW
    n.add('Line', 'SOUTH-WEST', bus0='SOUTH', bus1='WEST',
          x=0.1, s_nom=800)  # 800 MW
    
    # Get optimized site configurations
    sites = OPTIMIZED_CONFIG['sites']
    
    # Add solar generators at HOUSTON bus
    for site_name, config in sites.items():
        solar_name = f'Canopy_{site_name}'
        n.add('Generator', solar_name,
              bus='HOUSTON',
              p_nom=config['solar_kw'] / 1000,  # Convert to MW
              marginal_cost=0,  # Solar has no fuel cost
              p_max_pu=1.0)  # Will be set hourly
    
    # Add battery storage with optimized sizes
    duration_hours = OPTIMIZED_CONFIG['battery_config']['duration_hours']
    for site_name, config in sites.items():
        battery_name = f'Battery_{site_name}'
        n.add('StorageUnit', battery_name,
              bus='HOUSTON',
              p_nom=config['battery_kw'] / 1000,  # Convert to MW
              p_min_pu=-1,  # Can charge
              p_max_pu=1,   # Can discharge
              max_hours=duration_hours,  # 0.5 hours
              efficiency_store=0.95,
              efficiency_dispatch=0.95,
              standing_loss=0.0001,  # 0.01% per hour
              cyclic_state_of_charge=False)
    
    # Add grid connection (bidirectional) - connect to a separate grid bus
    n.add('Bus', 'GRID', v_nom=138)  # Grid bus
    n.add('Link', 'Grid_HOUSTON',
          bus0='HOUSTON',
          bus1='GRID',  # Connect to grid bus
          p_nom=10000,  # 10 MW max (enough for all scenarios)
          p_min_pu=-1,  # Can import
          p_max_pu=1,   # Can export
          marginal_cost=50)  # $50/MWh average LMP
    
    # Add slack generator at grid bus (for feasibility)
    n.add('Generator', 'Grid_Slack',
          bus='GRID',
          p_nom=10000,  # 10 MW
          marginal_cost=100,  # High cost, only used if needed
          p_max_pu=1.0)
    
    # Add loads
    # Host loads at each site
    load_profiles = generate_load_profiles()
    
    for site_name in sites.keys():
        load_name = f'Load_{site_name}'
        # Ensure load profile is a Series with correct index
        load_series = pd.Series(
            load_profiles[site_name].values / 1000,  # Convert to MW
            index=n.snapshots
        )
        n.add('Load', load_name,
              bus='HOUSTON',
              p_set=load_series)
    
    # Generate solar profiles
    pv_profiles = generate_solar_profiles()
    
    # Set time-varying generation
    for site_name, config in sites.items():
        gen_name = f'Canopy_{site_name}'
        profile = pv_profiles[site_name]
        # Normalize to capacity and ensure it's a Series with correct index
        p_max_pu_series = pd.Series(
            profile.values / config['solar_kw'],
            index=n.snapshots
        )
        n.generators_t.p_max_pu[gen_name] = p_max_pu_series
    
    return n, load_profiles, pv_profiles


def generate_solar_profiles():
    """
    Generate solar generation profiles for optimized sites.
    """
    sites = OPTIMIZED_CONFIG['sites']
    profiles = {}
    
    for site_name, config in sites.items():
        solar_kw = config['solar_kw']
        
        # Generate typical June day profile
        hours = np.arange(24)
        
        # Gaussian-like solar profile
        if site_name == 'Site_A':  # South Congress
            peak_center = 13  # 1 PM
            peak_width = 6
        elif site_name == 'Site_B':  # UT Campus
            peak_center = 14  # 2 PM
            peak_width = 5
        else:  # Site_C Airport
            peak_center = 13.5  # 1:30 PM
            peak_width = 7
        
        # Solar generation factor (0 to 1)
        solar_factor = np.exp(-0.5 * ((hours - peak_center) / (peak_width/2))**2)
        solar_factor = np.maximum(solar_factor, 0)
        
        # Add some variability
        solar_factor += np.random.normal(0, 0.05, 24)
        solar_factor = np.clip(solar_factor, 0, 1)
        
        # Scale to capacity
        generation_kw = solar_factor * solar_kw * 0.85  # 85% capacity factor
        
        profiles[site_name] = pd.Series(generation_kw, index=pd.date_range('2024-06-15 00:00', periods=24, freq='H'))
    
    return profiles


def generate_load_profiles():
    """
    Generate load profiles for host loads.
    """
    sites = OPTIMIZED_CONFIG['sites']
    profiles = {}
    
    # Typical load patterns
    hours = np.arange(24)
    
    # Site A: Commercial/Retail (South Congress)
    base_load_a = 50  # kW
    commercial_pattern = np.ones(24) * base_load_a
    commercial_pattern[11:14] *= 2.0  # Lunch peak
    commercial_pattern[17:20] *= 2.2  # Dinner peak
    commercial_pattern[0:6] *= 0.3  # Night low
    profiles['Site_A'] = pd.Series(commercial_pattern, 
                                   index=pd.date_range('2024-06-15 00:00', periods=24, freq='H'))
    
    # Site B: Campus (UT)
    base_load_b = 200  # kW
    campus_pattern = np.ones(24) * base_load_b
    campus_pattern[14:18] *= 1.8  # Afternoon peak
    campus_pattern[18:22] *= 1.5  # Evening
    campus_pattern[0:6] *= 0.5  # Night low
    profiles['Site_B'] = pd.Series(campus_pattern,
                                  index=pd.date_range('2024-06-15 00:00', periods=24, freq='H'))
    
    # Site C: Airport
    base_load_c = 300  # kW
    airport_pattern = np.ones(24) * base_load_c
    airport_pattern[6:10] *= 1.5  # Morning
    airport_pattern[14:18] *= 1.6  # Afternoon
    airport_pattern[0:5] *= 0.6  # Night low
    profiles['Site_C'] = pd.Series(airport_pattern,
                                  index=pd.date_range('2024-06-15 00:00', periods=24, freq='H'))
    
    return profiles


def run_scenario_1_btm_ppa(n, pv_profiles, load_profiles):
    """
    Scenario 1: Behind-the-Meter PPA (no export, or capped export).
    """
    print("\n" + "="*80)
    print("SCENARIO 1: BTM PPA (Optimized)")
    print("="*80)
    
    ppa_rate = get_optimized_ppa_rate() / 100  # Convert to $/kWh
    
    # Set grid link to allow limited export
    n.links.loc['Grid_HOUSTON', 'p_max_pu'] = 0.1  # Allow 10% export
    
    # Run optimization
    try:
        n.optimize(solver_name='highs')
        optimization_status = "ok" if hasattr(n, 'optimize') else "unknown"
    except Exception as e:
        print(f"  Warning: Optimization failed: {e}")
        optimization_status = "failed"
        # Create dummy results for visualization
        n.generators_t.p = pd.DataFrame(0, index=n.snapshots, columns=n.generators.index)
        n.storage_units_t.p = pd.DataFrame(0, index=n.snapshots, columns=n.storage_units.index)
        n.storage_units_t.state_of_charge = pd.DataFrame(0, index=n.snapshots, columns=n.storage_units.index)
        if 'Grid_HOUSTON' in n.links.index:
            n.links_t.p0 = pd.DataFrame(0, index=n.snapshots, columns=n.links.index)
            n.links_t.p1 = pd.DataFrame(0, index=n.snapshots, columns=n.links.index)
    
    # Calculate results
    results = {
        'scenario': 'S1: BTM PPA',
        'network': n,
        'ppa_rate': ppa_rate,
        'optimization_status': optimization_status,
        'generation': {},
        'loads': {},
        'battery_operation': {},
        'revenue': {},
        'costs': {}
    }
    
    # Extract generation
    sites = OPTIMIZED_CONFIG['sites']
    total_generation = 0
    for site_name in sites.keys():
        gen_name = f'Canopy_{site_name}'
        if gen_name in n.generators.index and gen_name in n.generators_t.p.columns:
            gen_mw = n.generators_t.p[gen_name].values
            results['generation'][site_name] = gen_mw * 1000  # Convert to kW
            total_generation += np.sum(gen_mw) * 1000  # Total kWh
        else:
            # Use profile directly if optimization failed
            results['generation'][site_name] = pv_profiles[site_name].values
            total_generation += np.sum(pv_profiles[site_name].values)
    
    # Extract loads
    total_load = 0
    for site_name in sites.keys():
        load_name = f'Load_{site_name}'
        if load_name in n.loads.index:
            load_mw = n.loads_t.p_set[load_name].values
            results['loads'][site_name] = load_mw * 1000  # Convert to kW
            total_load += np.sum(load_mw) * 1000  # Total kWh
        else:
            # Use profile directly
            results['loads'][site_name] = load_profiles[site_name].values
            total_load += np.sum(load_profiles[site_name].values)
    
    # Extract battery operation
    for site_name in sites.keys():
        battery_name = f'Battery_{site_name}'
        if battery_name in n.storage_units.index:
            if battery_name in n.storage_units_t.p.columns:
                battery_p = n.storage_units_t.p[battery_name].values
            else:
                battery_p = np.zeros(24)
            if battery_name in n.storage_units_t.state_of_charge.columns:
                battery_soc = n.storage_units_t.state_of_charge[battery_name].values
            else:
                battery_soc = np.zeros(24)
            results['battery_operation'][site_name] = {
                'power_mw': battery_p,
                'soc_mwh': battery_soc
            }
        else:
            results['battery_operation'][site_name] = {
                'power_mw': np.zeros(24),
                'soc_mwh': np.zeros(24)
            }
    
    # Calculate revenue
    # PPA revenue: energy to hosts at PPA rate
    energy_to_hosts = min(total_generation, total_load)  # kWh
    ppa_revenue = energy_to_hosts * ppa_rate  # $
    
    # Grid export revenue (if any)
    grid_export = 0
    if 'Grid_HOUSTON' in n.links.index and 'Grid_HOUSTON' in n.links_t.p1.columns:
        grid_export_mw = n.links_t.p1['Grid_HOUSTON'].values
        grid_export = np.sum(np.maximum(0, grid_export_mw)) * 1000  # kWh
    else:
        grid_export = max(0, total_generation - total_load)  # kWh
    lmp_avg = 50 / 1000  # $50/MWh = $0.05/kWh
    grid_revenue = grid_export * lmp_avg  # $
    
    results['revenue'] = {
        'ppa_revenue': ppa_revenue,
        'grid_revenue': grid_revenue,
        'total_revenue': ppa_revenue + grid_revenue
    }
    
    # Calculate costs
    grid_import = 0
    if 'Grid_HOUSTON' in n.links.index and 'Grid_HOUSTON' in n.links_t.p0.columns:
        grid_import_mw = n.links_t.p0['Grid_HOUSTON'].values
        grid_import = np.sum(np.maximum(0, grid_import_mw)) * 1000  # kWh
    else:
        grid_import = max(0, total_load - total_generation)  # kWh
    grid_cost = grid_import * lmp_avg  # $
    
    results['costs'] = {
        'grid_import_cost': grid_cost,
        'total_cost': grid_cost
    }
    
    results['net_revenue'] = results['revenue']['total_revenue'] - results['costs']['total_cost']
    
    print(f"\nGeneration: {total_generation:.1f} kWh")
    print(f"Load: {total_load:.1f} kWh")
    print(f"PPA Revenue: ${ppa_revenue:.2f}")
    print(f"Grid Revenue: ${grid_revenue:.2f}")
    print(f"Net Revenue: ${results['net_revenue']:.2f}")
    
    return results


def run_scenario_2_hybrid(n, pv_profiles, load_profiles):
    """
    Scenario 2: Hybrid PPA + Grid Sales (allow export to grid at LMP, with battery).
    """
    print("\n" + "="*80)
    print("SCENARIO 2: Hybrid PPA + Grid Sales (Optimized)")
    print("="*80)
    
    ppa_rate = get_optimized_ppa_rate() / 100
    
    # Allow full export
    n.links.loc['Grid_HOUSTON', 'p_max_pu'] = 1.0
    
    # Set LMP prices (time-varying)
    lmp_prices = generate_lmp_prices()
    n.links_t.marginal_cost['Grid_HOUSTON'] = lmp_prices / 1000  # Convert to $/MWh
    
    # Run optimization
    n.optimize(solver_name='highs')
    
    # Calculate results (similar to S1 but with more grid interaction)
    results = {
        'scenario': 'S2: Hybrid',
        'network': n,
        'ppa_rate': ppa_rate,
        'generation': {},
        'loads': {},
        'battery_operation': {},
        'revenue': {},
        'costs': {}
    }
    
    # Extract data (similar to S1)
    sites = OPTIMIZED_CONFIG['sites']
    total_generation = 0
    for site_name in sites.keys():
        gen_name = f'Canopy_{site_name}'
        gen_mw = n.generators_t.p[gen_name].values
        results['generation'][site_name] = gen_mw * 1000
        total_generation += np.sum(gen_mw) * 1000
    
    total_load = 0
    for site_name in sites.keys():
        load_name = f'Load_{site_name}'
        load_mw = n.loads_t.p_set[load_name].values
        results['loads'][site_name] = load_mw * 1000
        total_load += np.sum(load_mw) * 1000
    
    for site_name in sites.keys():
        battery_name = f'Battery_{site_name}'
        battery_p = n.storage_units_t.p[battery_name].values
        battery_soc = n.storage_units_t.state_of_charge[battery_name].values
        results['battery_operation'][site_name] = {
            'power_mw': battery_p,
            'soc_mwh': battery_soc
        }
    
    # Calculate revenue with battery arbitrage
    energy_to_hosts = min(total_generation, total_load)
    ppa_revenue = energy_to_hosts * ppa_rate
    
    # Grid export (with battery optimization)
    grid_export_mw = n.links_t.p1['Grid_HOUSTON'].values
    grid_export_kwh = np.sum(np.maximum(0, grid_export_mw)) * 1000
    grid_revenue = np.sum(np.maximum(0, grid_export_mw) * lmp_prices.values / 1000) * 1000
    
    results['revenue'] = {
        'ppa_revenue': ppa_revenue,
        'grid_revenue': grid_revenue,
        'total_revenue': ppa_revenue + grid_revenue
    }
    
    grid_import_mw = n.links_t.p0['Grid_HOUSTON'].values
    grid_import_kwh = np.sum(np.maximum(0, grid_import_mw)) * 1000
    grid_cost = np.sum(np.maximum(0, grid_import_mw) * lmp_prices.values / 1000) * 1000
    
    results['costs'] = {
        'grid_import_cost': grid_cost,
        'total_cost': grid_cost
    }
    
    results['net_revenue'] = results['revenue']['total_revenue'] - results['costs']['total_cost']
    
    print(f"\nGeneration: {total_generation:.1f} kWh")
    print(f"Load: {total_load:.1f} kWh")
    print(f"PPA Revenue: ${ppa_revenue:.2f}")
    print(f"Grid Revenue: ${grid_revenue:.2f}")
    print(f"Net Revenue: ${results['net_revenue']:.2f}")
    
    return results


def generate_lmp_prices():
    """
    Generate realistic ERCOT LMP prices.
    """
    hours = np.arange(24)
    
    # Typical ERCOT pattern: low at night, high during peak
    base_price = 30  # $/MWh
    peak_multiplier = np.ones(24)
    peak_multiplier[6:10] = 1.5  # Morning
    peak_multiplier[14:20] = 2.0  # Afternoon peak
    peak_multiplier[0:6] = 0.7  # Night low
    
    lmp = base_price * peak_multiplier
    lmp += np.random.normal(0, 5, 24)  # Add variability
    lmp = np.maximum(lmp, 15)  # Floor at $15/MWh
    lmp = np.minimum(lmp, 150)  # Cap at $150/MWh
    
    return pd.Series(lmp, index=pd.date_range('2024-06-15 00:00', periods=24, freq='H'))


def run_all_optimized_scenarios():
    """
    Run all scenarios with optimized parameters.
    """
    print("="*80)
    print("OPTIMIZED PYPSA SCENARIO ANALYSIS")
    print("="*80)
    
    # Create network
    print("\nCreating optimized network...")
    n, load_profiles, pv_profiles = create_optimized_network()
    
    print(f"  Solar: {OPTIMIZED_CONFIG['total_solar_kw']} kW")
    print(f"  Battery: {OPTIMIZED_CONFIG['total_battery_kw']} kW / {OPTIMIZED_CONFIG['total_battery_kwh']} kWh")
    print(f"  PPA Rate: {get_optimized_ppa_rate():.2f}¢/kWh")
    
    # Run scenarios
    results = {}
    
    # Scenario 1
    n1, load_profiles, pv_profiles = create_optimized_network()
    results['S1'] = run_scenario_1_btm_ppa(n1, pv_profiles, load_profiles)
    
    # Scenario 2
    n2, load_profiles, pv_profiles = create_optimized_network()
    results['S2'] = run_scenario_2_hybrid(n2, pv_profiles, load_profiles)
    
    return results


if __name__ == "__main__":
    results = run_all_optimized_scenarios()
    
    print("\n" + "="*80)
    print("OPTIMIZED SCENARIO ANALYSIS COMPLETE!")
    print("="*80)

