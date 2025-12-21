# ParkUrban API Backend

Real-time parking data API with forecasting capabilities. Designed to start with simulated data and easily swap to real sensor feeds.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Initialize Database

```bash
npm run setup-db
```

Or the database will auto-initialize on first run.

### 3. Start Data Ingestion (Simulated Data)

In one terminal:
```bash
npm run ingest
```

This simulates sensor data every 30 seconds.

### 4. Start API Server

In another terminal:
```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

## API Endpoints

### Health Check
```
GET /health
```

### Get All Lots
```
GET /api/lots
```

Returns:
```json
{
  "lots": [
    {
      "lot_id": "lot1",
      "name": "Lot 1 - Speedway",
      "capacity": 450,
      "shaded_capacity": 180,
      "current_occupied": 382,
      "current_open": 68,
      "occupancy_percent": "84.9",
      "shaded_open": 12,
      "ev_available": 2,
      "ev_total": 3,
      "last_updated": "2025-01-15T10:30:00.000Z"
    }
  ]
}
```

### Get Forecast
```
GET /api/forecast?lot_id=lot1
```

Returns:
```json
{
  "lot_id": "lot1",
  "lot_name": "Lot 1 - Speedway",
  "forecasts": {
    "15": {
      "predicted_open": 45,
      "predicted_occupied": 405,
      "confidence": 0.75,
      "method": "weighted_average"
    },
    "30": { ... },
    "60": { ... }
  },
  "generated_at": "2025-01-15T10:30:00.000Z"
}
```

### Get EV Charger Status
```
GET /api/ev
GET /api/ev?lot_id=lot1
```

Returns:
```json
{
  "chargers": [
    {
      "charger_id": "ev1",
      "lot_id": "lot1",
      "name": "Charger 1",
      "status": "available",
      "power_kw": 7.2,
      "last_updated": "2025-01-15T10:30:00.000Z"
    }
  ],
  "summary": {
    "total": 6,
    "available": 4,
    "in_use": 1,
    "out_of_service": 1
  }
}
```

### Get Lot Details
```
GET /api/lots/:lot_id
```

## Architecture

```
┌─────────────────┐
│  Data Sources   │
│  (Simulated or  │
│   Real Sensors) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Ingestion  │
│   (Cron Job)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SQLite DB     │
│  (parkurban.db) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Express API    │
│   (REST Endpoints)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frontend       │
│  (parkurban.html)│
└─────────────────┘
```

## Replacing Simulated Data with Real Sources

### Option 1: Camera/Vendor API

Edit `data-ingestion.js`:

```javascript
// Replace simulateOccupancy() with:
async function fetchFromCameraAPI(lot_id) {
    const response = await axios.get(`https://camera-vendor-api.com/lots/${lot_id}`);
    return {
        occupied: response.data.occupied_count,
        shaded_occupied: response.data.shaded_occupied_count
    };
}
```

### Option 2: EV Charger Network API

```javascript
// Replace simulateEVStatus() with:
async function fetchFromChargePoint(lot_id) {
    const response = await axios.get(`https://api.chargepoint.com/stations`, {
        headers: { 'Authorization': `Bearer ${API_KEY}` }
    });
    // Map response to charger status
}
```

### Option 3: Manual Updates (Google Sheets)

You can create a simple endpoint to accept manual updates:

```javascript
app.post('/api/admin/update-occupancy', async (req, res) => {
    const { lot_id, occupied, shaded_occupied } = req.body;
    await db.insertOccupancy(lot_id, occupied, shaded_occupied);
    res.json({ success: true });
});
```

## Deployment

### Option 1: Render.com (Recommended for MVP)

1. Create account at render.com
2. Connect GitHub repository
3. Set build command: `cd backend && npm install`
4. Set start command: `cd backend && npm start`
5. Add environment variable: `PORT=3000`

### Option 2: Railway

1. Create account at railway.app
2. Deploy from GitHub
3. Set root directory to `backend`
4. Railway auto-detects Node.js

### Option 3: Fly.io

```bash
cd backend
fly launch
fly deploy
```

### Option 4: AWS Lightsail

1. Create Node.js instance
2. SSH into instance
3. Clone repo and run setup

## Environment Variables

Create `.env` file:

```
PORT=3000
NODE_ENV=production
DB_PATH=./parkurban.db
```

## Database Schema

- **lots**: Lot metadata (capacity, shaded spots, location)
- **occupancy**: Time-series occupancy data
- **ev_chargers**: EV charger status
- **forecasts**: Cached predictions

## Next Steps

1. ✅ Deploy backend to cloud (Render/Railway)
2. ✅ Update frontend to call API
3. ✅ Replace simulated data with real sources
4. ✅ Add authentication for admin endpoints
5. ✅ Add monitoring and alerts
