# Archive

This folder contains earlier versions of the DER Exchange model that have been superseded by the PyPSA implementation.

## Archived Files

### 1. `urban_der_exchange.py`
- **Version**: 1.0
- **Date**: November 2025
- **Description**: Original simplified model with synthetic solar profiles
- **Status**: ✅ Working, but superseded by PyPSA models
- **Use Case**: Quick demonstrations without API keys

### 2. `urban_der_exchange_with_nrel.py`
- **Version**: 1.1
- **Date**: November 2025
- **Description**: Attempted NSRDB API integration
- **Status**: ⚠️ NSRDB endpoint deprecated, use PVWatts instead
- **Note**: Kept for reference on NSRDB data structures

### 3. `urban_der_exchange_with_pvwatts.py`
- **Version**: 1.2
- **Date**: November 2025
- **Description**: First successful NREL PVWatts integration
- **Status**: ✅ Working, but simplified (no PyPSA optimization)
- **Use Case**: Quick PVWatts data testing

### 4. `demo_with_sample_nrel_data.py`
- **Version**: 1.3
- **Date**: November 2025
- **Description**: Realistic profiles based on NREL characteristics
- **Status**: ✅ Working, no API key needed
- **Use Case**: Demo when NREL API is unavailable

### 5. `example_usage.py`
- **Version**: 1.x
- **Date**: November 2025
- **Description**: Usage examples for v1.x models
- **Status**: ✅ Working with archived models
- **Note**: See main README for v2.0 usage

## Why Archived?

These files were replaced by the PyPSA implementation (`../pypsa_models/`) which provides:
- ✅ Proper network optimization (LOPF)
- ✅ Multi-scenario comparison
- ✅ Battery dispatch optimization
- ✅ Grid-integrated modeling
- ✅ Academic rigor for papers

## Can I Still Use These?

Yes! All archived files are fully functional. To use:

```bash
cd archive
python urban_der_exchange.py
```

However, for new work, we recommend using the PyPSA models.

---

**Last Updated**: November 2025  
**Status**: Archived but functional

