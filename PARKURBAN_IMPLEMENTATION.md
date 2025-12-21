# ParkUrban Implementation Guide

## 🎯 Overview

This guide shows you how to build **exactly what your ParkUrban page shows** - live counts, shaded spots, EV status, and 15/30/60 minute forecasts - starting with simulated data and scaling to real sensors.

---

## 📁 Project Structure

```
LandingPage_SunnyGrids/
├── backend/                    # API Server
│   ├── server.js              # Express API server
│   ├── database.js            # SQLite database operations
│   ├── forecasting.js         # 15/30/60 min prediction models
│   ├── data-ingestion.js      # Simulated sensor data (replace with real)
│   ├── package.json           # Dependencies
│   ├── scripts/
│   │   └── setup-database.js  # Database initialization
│   └── DEPLOYMENT.md          # Deployment instructions
│
├── landing_page/
│   ├── parkurban.html         # Main ParkUrban page (updated with API)
│   ├── parkurban-api.js       # API client (fetches from backend)
│   └── [other pages]
│
└── docs/
    └── PARKURBAN_STANDALONE_IMPLEMENTATION.md  # Business strategy
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Backend

```bash
cd backend
npm install
npm run setup-db
```

### Step 2: Start Data Ingestion (Terminal 1)

```bash
npm run ingest
```

This simulates sensor data every 30 seconds.

### Step 3: Start API Server (Terminal 2)

```bash
npm start
```

API is now running at: `http://localhost:3000`

### Step 4: Test API

Open in browser:
- Health: http://localhost:3000/health
- Lots: http://localhost:3000/api/lots
- Forecast: http://localhost:3000/api/forecast?lot_id=lot1

### Step 5: View Frontend

Open `landing_page/parkurban.html` in your browser. The page will:
- Fetch real data from API
- Display live counts
- Show forecasts
- Update every 30 seconds

---

## 📊 What You Get

### API Endpoints

**GET /api/lots**
```json
{
  "lots": [
    {
      "lot_id": "lot1",
      "name": "Lot 1 - Speedway",
      "capacity": 450,
      "current_open": 68,
      "shaded_open": 12,
      "ev_available": 2,
      "ev_total": 3,
      "last_updated": "2025-01-15T10:30:00.000Z"
    }
  ]
}
```

**GET /api/forecast?lot_id=lot1**
```json
{
  "forecasts": {
    "15": { "predicted_open": 45, "confidence": 0.75 },
    "30": { "predicted_open": 52, "confidence": 0.70 },
    "60": { "predicted_open": 68, "confidence": 0.65 }
  }
}
```

**GET /api/ev**
```json
{
  "chargers": [
    {
      "charger_id": "ev1",
      "lot_id": "lot1",
      "status": "available",
      "power_kw": 7.2
    }
  ],
  "summary": {
    "total": 6,
    "available": 4,
    "in_use": 1
  }
}
```

---

## 🔄 Replacing Simulated Data with Real Sources

### Option 1: Camera/Vendor API (Recommended)

Edit `backend/data-ingestion.js`:

```javascript
const axios = require('axios');

async function fetchFromCameraAPI(lot_id) {
    const response = await axios.get(`https://camera-vendor-api.com/lots/${lot_id}`, {
        headers: { 'Authorization': `Bearer ${CAMERA_API_KEY}` }
    });
    
    return {
        occupied: response.data.occupied_count,
        shaded_occupied: response.data.shaded_occupied_count
    };
}

// Replace in ingestOccupancy():
const occupancy = await fetchFromCameraAPI(lot.lot_id);
await db.insertOccupancy(lot.lot_id, occupancy.occupied, occupancy.shaded_occupied);
```

### Option 2: EV Charger Network API

```javascript
async function fetchFromChargePoint(lot_id) {
    const response = await axios.get(`https://api.chargepoint.com/stations`, {
        params: { location_id: lot_id },
        headers: { 'Authorization': `Bearer ${CHARGE_POINT_API_KEY}` }
    });
    
    return response.data.stations.map(station => ({
        charger_id: station.id,
        lot_id: lot_id,
        status: station.status === 'Available' ? 'available' : 'in_use',
        power_kw: station.power_kw
    }));
}
```

### Option 3: Manual Updates (Google Sheets)

Add endpoint to `backend/server.js`:

```javascript
app.post('/api/admin/update-occupancy', async (req, res) => {
    const { lot_id, occupied, shaded_occupied } = req.body;
    await db.insertOccupancy(lot_id, occupied, shaded_occupied);
    res.json({ success: true });
});
```

Then use Google Apps Script or Zapier to POST to this endpoint.

---

## 🌐 Deploy to Production

### Deploy Backend (Render.com - Free)

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - Root Directory: `backend`
   - Build: `npm install`
   - Start: `npm start`
5. Deploy!

**Your API URL**: `https://parkurban-api.onrender.com`

### Update Frontend

Edit `landing_page/parkurban-api.js`:

```javascript
const API_CONFIG = {
    baseURL: 'https://parkurban-api.onrender.com', // Your deployed URL
    useSimulatedData: true // Keep as fallback
};
```

---

## 📈 Forecasting Model

The forecasting uses a **weighted average** of three methods:

1. **Last-week same time** (50% weight) - Most reliable baseline
2. **Recent trend** (30% weight) - Last hour average
3. **Time-of-day pattern** (20% weight) - Hourly patterns

**Confidence** decreases for longer horizons:
- 15 min: ~75% confidence
- 30 min: ~70% confidence
- 60 min: ~65% confidence

### Improving Forecasts

Add more sophisticated models in `backend/forecasting.js`:

```javascript
// Option: XGBoost (requires training data)
// Option: Prophet (Facebook's time-series)
// Option: LSTM (neural network, needs lots of data)
```

---

## 🎨 Frontend Features

### Mobile Mockup Updates

- ✅ **Live "Available Now" count** - Updates from API
- ✅ **Lot cards** - Real occupancy data
- ✅ **Shaded spots** - Dynamic count
- ✅ **EV charger status** - Real-time availability
- ✅ **15/30/60 min forecasts** - Predictive availability

### Demo Section Updates

- ✅ **Parking grid** - Real occupancy visualization
- ✅ **Global stats** - Total spots, vacant count, occupancy %
- ✅ **Auto-refresh** - Updates every 30 seconds

---

## 🔧 Architecture

```
┌─────────────────────────────────────────┐
│         Data Sources                    │
│  (Simulated → Real Sensors/Cameras)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Data Ingestion Service             │
│      (Runs every 30 seconds)            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         SQLite Database                 │
│  (lots, occupancy, ev_chargers, etc.)   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Express API Server               │
│  /api/lots, /api/forecast, /api/ev     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Frontend (parkurban.html)       │
│  Fetches data, displays live counts     │
└─────────────────────────────────────────┘
```

---

## 📝 Next Steps

### Week 1: Get It Running
- [x] Setup backend locally
- [x] Test API endpoints
- [x] Verify frontend connects
- [ ] Deploy backend to cloud

### Week 2: Add Real Data Source
- [ ] Choose data source (camera API, sensors, manual)
- [ ] Replace simulated data in `data-ingestion.js`
- [ ] Test with real data
- [ ] Monitor accuracy

### Week 3: Improve Forecasting
- [ ] Collect more historical data
- [ ] Train better models
- [ ] Add confidence intervals
- [ ] A/B test forecast accuracy

### Week 4: Pilot Deployment
- [ ] Deploy to 1 real lot
- [ ] Install sensors/cameras
- [ ] Monitor and iterate
- [ ] Gather user feedback

---

## 🐛 Troubleshooting

### API Not Responding

```bash
# Check if server is running
curl http://localhost:3000/health

# Check data ingestion
# Should see logs every 30 seconds
```

### Frontend Shows "Simulated Data"

- Check browser console for errors
- Verify API URL in `parkurban-api.js`
- Check CORS settings (API has CORS enabled)
- Verify API is running

### Database Issues

```bash
# Reset database
rm backend/parkurban.db
npm run setup-db
```

---

## 📚 Additional Resources

- **Backend README**: `backend/README.md`
- **Deployment Guide**: `backend/DEPLOYMENT.md`
- **Business Strategy**: `docs/PARKURBAN_STANDALONE_IMPLEMENTATION.md`

---

## ✅ What's Built

- ✅ **Backend API** - Express server with SQLite
- ✅ **Data Ingestion** - Simulated sensor data (ready for real sources)
- ✅ **Forecasting** - 15/30/60 min predictions
- ✅ **Frontend Integration** - ParkUrban page consumes API
- ✅ **Auto-refresh** - Updates every 30 seconds
- ✅ **Fallback** - Simulated data if API unavailable

**Ready to demo and scale!** 🚀
