/**
 * Data Ingestion Service
 * Simulates real-time data collection from sensors/cameras/APIs
 * Can be replaced with actual data sources later
 */

const cron = require('node-cron');
const db = require('./database');

// Simulated lot configurations (UT Campus)
const LOTS = [
    {
        lot_id: 'lot1',
        name: 'Lot 1 - Speedway',
        capacity: 450,
        shaded_capacity: 180,
        latitude: 30.2856,
        longitude: -97.7394
    },
    {
        lot_id: 'lot2',
        name: 'Lot 2 - San Jacinto',
        capacity: 320,
        shaded_capacity: 128,
        latitude: 30.2870,
        longitude: -97.7370
    },
    {
        lot_id: 'lot3',
        name: 'Lot 3 - East Campus',
        capacity: 280,
        shaded_capacity: 112,
        latitude: 30.2830,
        longitude: -97.7350
    }
];

// EV Charger configurations
const EV_CHARGERS = [
    { charger_id: 'ev1', lot_id: 'lot1', name: 'Charger 1', power_kw: 7.2 },
    { charger_id: 'ev2', lot_id: 'lot1', name: 'Charger 2', power_kw: 7.2 },
    { charger_id: 'ev3', lot_id: 'lot1', name: 'Charger 3', power_kw: 11.0 },
    { charger_id: 'ev4', lot_id: 'lot2', name: 'Charger 1', power_kw: 7.2 },
    { charger_id: 'ev5', lot_id: 'lot2', name: 'Charger 2', power_kw: 11.0 },
    { charger_id: 'ev6', lot_id: 'lot3', name: 'Charger 1', power_kw: 7.2 }
];

// Initialize lots in database
async function initializeLots() {
    const sqlite3 = require('sqlite3').verbose();
    const path = require('path');
    const db = new sqlite3.Database(path.join(__dirname, 'parkurban.db'));
    
    return new Promise((resolve) => {
        db.serialize(() => {
            LOTS.forEach(lot => {
                db.run(
                    `INSERT OR IGNORE INTO lots (lot_id, name, capacity, shaded_capacity, latitude, longitude)
                     VALUES (?, ?, ?, ?, ?, ?)`,
                    [lot.lot_id, lot.name, lot.capacity, lot.shaded_capacity, lot.latitude, lot.longitude]
                );
            });
            
            EV_CHARGERS.forEach(charger => {
                db.run(
                    `INSERT OR IGNORE INTO ev_chargers (charger_id, lot_id, name, status, power_kw)
                     VALUES (?, ?, ?, 'available', ?)`,
                    [charger.charger_id, charger.lot_id, charger.name, charger.power_kw]
                );
            });
            
            db.close(() => resolve());
        });
    });
}

// Simulate occupancy based on time of day and day of week
function simulateOccupancy(lot, timestamp) {
    const date = new Date(timestamp);
    const hour = date.getHours();
    const dayOfWeek = date.getDay();
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    
    // Base occupancy patterns
    let baseOccupancy = 0.3; // 30% base
    
    // Peak hours: 8-10 AM, 12-2 PM, 5-7 PM
    if (hour >= 8 && hour <= 10) baseOccupancy = 0.85; // Morning rush
    else if (hour >= 12 && hour <= 14) baseOccupancy = 0.75; // Lunch
    else if (hour >= 17 && hour <= 19) baseOccupancy = 0.80; // Evening
    else if (hour >= 22 || hour <= 6) baseOccupancy = 0.10; // Late night
    
    // Weekends are less busy
    if (isWeekend) baseOccupancy *= 0.4;
    
    // Add some randomness (±10%)
    const variation = (Math.random() - 0.5) * 0.2;
    const occupancyRate = Math.max(0, Math.min(1, baseOccupancy + variation));
    
    const occupied = Math.round(lot.capacity * occupancyRate);
    const shadedOccupied = Math.round(lot.shaded_capacity * occupancyRate * 1.1); // Shaded spots are more popular
    
    return {
        occupied: Math.min(occupied, lot.capacity),
        shaded_occupied: Math.min(shadedOccupied, lot.shaded_capacity)
    };
}

// Simulate EV charger status
function simulateEVStatus() {
    const statuses = ['available', 'in_use', 'available', 'available', 'out_of_service']; // 60% available, 20% in use, 20% out
    const weights = [0.6, 0.2, 0.6, 0.6, 0.05];
    
    return statuses[Math.floor(Math.random() * statuses.length)];
}

// Ingest occupancy data
async function ingestOccupancy() {
    console.log(`[${new Date().toISOString()}] Ingesting occupancy data...`);
    
    try {
        for (const lot of LOTS) {
            const occupancy = simulateOccupancy(lot, new Date());
            await db.insertOccupancy(lot.lot_id, occupancy.occupied, occupancy.shaded_occupied);
            console.log(`  ✓ ${lot.name}: ${occupancy.occupied}/${lot.capacity} occupied`);
        }
    } catch (error) {
        console.error('Error ingesting occupancy:', error);
    }
}

// Ingest EV charger status
async function ingestEVStatus() {
    console.log(`[${new Date().toISOString()}] Ingesting EV charger status...`);
    
    try {
        for (const charger of EV_CHARGERS) {
            const status = simulateEVStatus();
            await db.updateEVStatus(charger.charger_id, status);
        }
        console.log(`  ✓ Updated ${EV_CHARGERS.length} EV chargers`);
    } catch (error) {
        console.error('Error ingesting EV status:', error);
    }
}

// Main ingestion function
async function runIngestion() {
    await ingestOccupancy();
    await ingestEVStatus();
}

// Initialize and start
async function start() {
    console.log('🚀 Starting ParkUrban Data Ingestion Service...');
    
    // Initialize database with lots and chargers
    await initializeLots();
    console.log('✓ Database initialized');
    
    // Run initial ingestion
    await runIngestion();
    
    // Schedule periodic ingestion (every 30 seconds for demo, can be adjusted)
    cron.schedule('*/30 * * * * *', async () => {
        await runIngestion();
    });
    
    console.log('✓ Ingestion service running (updates every 30 seconds)');
    console.log('Press Ctrl+C to stop');
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n👋 Shutting down ingestion service...');
    process.exit(0);
});

// Start the service
start().catch(console.error);
