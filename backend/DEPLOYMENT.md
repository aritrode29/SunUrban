# ParkUrban API Deployment Guide

## Quick Start (Local Development)

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Setup Database

```bash
npm run setup-db
```

This creates the database and populates it with:
- 3 sample lots (UT Campus)
- 6 EV chargers
- 7 days of historical occupancy data (for forecasting)

### 3. Start Data Ingestion (Terminal 1)

```bash
npm run ingest
```

This simulates sensor data every 30 seconds.

### 4. Start API Server (Terminal 2)

```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

### 5. Update Frontend API URL

Edit `landing_page/parkurban-api.js`:

```javascript
const API_CONFIG = {
    baseURL: 'http://localhost:3000', // Local development
    useSimulatedData: true // Fallback if API unavailable
};
```

### 6. Test

- API: http://localhost:3000/api/lots
- Frontend: Open `landing_page/parkurban.html` in browser

---

## Deploy to Production

### Option 1: Render.com (Recommended - Free Tier Available)

1. **Create Account**: https://render.com
2. **New Web Service**:
   - Connect GitHub repository
   - Root Directory: `backend`
   - Build Command: `npm install`
   - Start Command: `npm start`
   - Environment: Node
3. **Environment Variables**:
   - `PORT`: 3000 (auto-set by Render)
   - `NODE_ENV`: production
4. **Deploy**: Render will auto-deploy on push to main

**Your API URL**: `https://parkurban-api.onrender.com`

### Option 2: Railway

1. **Create Account**: https://railway.app
2. **New Project** → Deploy from GitHub
3. **Settings**:
   - Root Directory: `backend`
   - Build Command: `npm install`
   - Start Command: `npm start`
4. **Deploy**: Railway auto-detects Node.js

**Your API URL**: `https://your-project.railway.app`

### Option 3: Fly.io

```bash
cd backend
fly launch
fly deploy
```

### Option 4: AWS Lightsail

1. Create Node.js instance
2. SSH and clone repo
3. Run setup commands
4. Use PM2 for process management

---

## Update Frontend for Production

After deploying, update `landing_page/parkurban-api.js`:

```javascript
const API_CONFIG = {
    baseURL: 'https://your-api-url.onrender.com', // Your deployed API
    useSimulatedData: true // Keep as fallback
};
```

---

## Replace Simulated Data with Real Sources

### Step 1: Camera/Vendor API

Edit `backend/data-ingestion.js`:

```javascript
// Replace simulateOccupancy() with:
async function fetchFromCameraAPI(lot_id) {
    const response = await axios.get(`https://camera-vendor-api.com/lots/${lot_id}`, {
        headers: { 'Authorization': `Bearer ${API_KEY}` }
    });
    return {
        occupied: response.data.occupied_count,
        shaded_occupied: response.data.shaded_occupied_count
    };
}
```

### Step 2: EV Charger Network API

```javascript
// Replace simulateEVStatus() with:
async function fetchFromChargePoint(lot_id) {
    const response = await axios.get(`https://api.chargepoint.com/stations`, {
        params: { location_id: lot_id },
        headers: { 'Authorization': `Bearer ${CHARGE_POINT_API_KEY}` }
    });
    // Map response to charger status
    return response.data.stations.map(station => ({
        charger_id: station.id,
        lot_id: lot_id,
        status: station.status === 'Available' ? 'available' : 'in_use',
        power_kw: station.power_kw
    }));
}
```

### Step 3: Manual Updates (Google Sheets)

Add endpoint to `backend/server.js`:

```javascript
app.post('/api/admin/update-occupancy', async (req, res) => {
    const { lot_id, occupied, shaded_occupied } = req.body;
    await db.insertOccupancy(lot_id, occupied, shaded_occupied);
    res.json({ success: true });
});
```

---

## Monitoring & Maintenance

### Check API Health

```bash
curl http://localhost:3000/health
```

### View Database

Use SQLite browser or command line:

```bash
sqlite3 backend/parkurban.db
.tables
SELECT * FROM lots;
SELECT * FROM occupancy ORDER BY timestamp DESC LIMIT 10;
```

### Logs

- Render: View in dashboard
- Railway: View in dashboard
- Local: Check console output

---

## Troubleshooting

### API Not Responding

1. Check if server is running: `curl http://localhost:3000/health`
2. Check data ingestion is running
3. Verify database exists: `ls backend/parkurban.db`

### CORS Errors

The API has CORS enabled. If issues persist, check:
- API URL is correct
- API server is running
- Browser console for errors

### Database Locked

SQLite can lock if multiple processes access it. Solution:
- Use one ingestion process
- Or migrate to PostgreSQL (for production)

---

## Next Steps

1. ✅ Deploy backend to cloud
2. ✅ Update frontend API URL
3. ✅ Test end-to-end
4. ✅ Replace simulated data with real sources
5. ✅ Add authentication
6. ✅ Add monitoring/alerts
