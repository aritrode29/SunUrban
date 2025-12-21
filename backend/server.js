const express = require('express');
const cors = require('cors');
const db = require('./database');
const { generateForecast } = require('./forecasting');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get all lots with current status
app.get('/api/lots', async (req, res) => {
    try {
        const lots = await db.getAllLots();
        const lotsWithStatus = await Promise.all(lots.map(async (lot) => {
            const occupancy = await db.getLatestOccupancy(lot.lot_id);
            const evStatus = await db.getEVStatusForLot(lot.lot_id);
            
            return {
                ...lot,
                current_occupied: occupancy?.occupied || 0,
                current_open: lot.capacity - (occupancy?.occupied || 0),
                occupancy_percent: ((occupancy?.occupied || 0) / lot.capacity * 100).toFixed(1),
                shaded_open: lot.shaded_capacity - (occupancy?.shaded_occupied || 0),
                ev_available: evStatus.filter(e => e.status === 'available').length,
                ev_total: evStatus.length,
                last_updated: occupancy?.timestamp || new Date().toISOString()
            };
        }));
        
        res.json({ lots: lotsWithStatus });
    } catch (error) {
        console.error('Error fetching lots:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get forecast for a specific lot
app.get('/api/forecast', async (req, res) => {
    try {
        const { lot_id } = req.query;
        if (!lot_id) {
            return res.status(400).json({ error: 'lot_id is required' });
        }
        
        const lot = await db.getLot(lot_id);
        if (!lot) {
            return res.status(404).json({ error: 'Lot not found' });
        }
        
        // Get historical data for forecasting
        const history = await db.getOccupancyHistory(lot_id, 7); // Last 7 days
        
        // Generate forecasts
        const forecasts = {
            '15': generateForecast(history, lot, 15),
            '30': generateForecast(history, lot, 30),
            '60': generateForecast(history, lot, 60)
        };
        
        res.json({
            lot_id,
            lot_name: lot.name,
            forecasts,
            generated_at: new Date().toISOString()
        });
    } catch (error) {
        console.error('Error generating forecast:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get EV charger status
app.get('/api/ev', async (req, res) => {
    try {
        const { lot_id } = req.query;
        
        let evStatus;
        if (lot_id) {
            evStatus = await db.getEVStatusForLot(lot_id);
        } else {
            evStatus = await db.getAllEVStatus();
        }
        
        res.json({
            chargers: evStatus,
            summary: {
                total: evStatus.length,
                available: evStatus.filter(e => e.status === 'available').length,
                in_use: evStatus.filter(e => e.status === 'in_use').length,
                out_of_service: evStatus.filter(e => e.status === 'out_of_service').length
            }
        });
    } catch (error) {
        console.error('Error fetching EV status:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get detailed lot information
app.get('/api/lots/:lot_id', async (req, res) => {
    try {
        const { lot_id } = req.params;
        const lot = await db.getLot(lot_id);
        
        if (!lot) {
            return res.status(404).json({ error: 'Lot not found' });
        }
        
        const occupancy = await db.getLatestOccupancy(lot_id);
        const evStatus = await db.getEVStatusForLot(lot_id);
        const history = await db.getOccupancyHistory(lot_id, 24); // Last 24 hours
        
        res.json({
            ...lot,
            current_occupied: occupancy?.occupied || 0,
            current_open: lot.capacity - (occupancy?.occupied || 0),
            shaded_open: lot.shaded_capacity - (occupancy?.shaded_occupied || 0),
            ev_chargers: evStatus,
            recent_history: history,
            last_updated: occupancy?.timestamp || new Date().toISOString()
        });
    } catch (error) {
        console.error('Error fetching lot details:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 ParkUrban API server running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(`📍 Lots endpoint: http://localhost:${PORT}/api/lots`);
});
