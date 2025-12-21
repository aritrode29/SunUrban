/**
 * Database Setup Script
 * Initializes the database with sample lots and chargers
 */

const db = require('../database');
const path = require('path');

async function setupDatabase() {
    console.log('🔧 Setting up ParkUrban database...');
    
    // Initialize database schema first
    await new Promise((resolve, reject) => {
        const db = require('../database');
        setTimeout(resolve, 1000); // Wait for schema initialization
    });
    
    const sqlite3 = require('sqlite3').verbose();
    const dbPath = path.join(__dirname, '..', 'parkurban.db');
    const database = new sqlite3.Database(dbPath);
    
    return new Promise((resolve, reject) => {
        database.serialize(() => {
            // Insert sample lots
            const lots = [
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
            
            lots.forEach(lot => {
                database.run(
                    `INSERT OR REPLACE INTO lots (lot_id, name, capacity, shaded_capacity, latitude, longitude)
                     VALUES (?, ?, ?, ?, ?, ?)`,
                    [lot.lot_id, lot.name, lot.capacity, lot.shaded_capacity, lot.latitude, lot.longitude],
                    (err) => {
                        if (err) console.error(`Error inserting lot ${lot.lot_id}:`, err);
                        else console.log(`✓ Added lot: ${lot.name}`);
                    }
                );
            });
            
            // Insert EV chargers
            const chargers = [
                { charger_id: 'ev1', lot_id: 'lot1', name: 'Charger 1', power_kw: 7.2 },
                { charger_id: 'ev2', lot_id: 'lot1', name: 'Charger 2', power_kw: 7.2 },
                { charger_id: 'ev3', lot_id: 'lot1', name: 'Charger 3', power_kw: 11.0 },
                { charger_id: 'ev4', lot_id: 'lot2', name: 'Charger 1', power_kw: 7.2 },
                { charger_id: 'ev5', lot_id: 'lot2', name: 'Charger 2', power_kw: 11.0 },
                { charger_id: 'ev6', lot_id: 'lot3', name: 'Charger 1', power_kw: 7.2 }
            ];
            
            chargers.forEach(charger => {
                database.run(
                    `INSERT OR REPLACE INTO ev_chargers (charger_id, lot_id, name, status, power_kw)
                     VALUES (?, ?, ?, 'available', ?)`,
                    [charger.charger_id, charger.lot_id, charger.name, charger.power_kw],
                    (err) => {
                        if (err) console.error(`Error inserting charger ${charger.charger_id}:`, err);
                        else console.log(`✓ Added charger: ${charger.name} (${charger.lot_id})`);
                    }
                );
            });
            
            // Generate some initial occupancy history (last 7 days)
            console.log('📊 Generating sample occupancy history...');
            const now = Date.now();
            const sevenDaysAgo = now - (7 * 24 * 60 * 60 * 1000);
            
            lots.forEach(lot => {
                // Generate hourly data points for last 7 days
                for (let time = sevenDaysAgo; time < now; time += 60 * 60 * 1000) {
                    const date = new Date(time);
                    const hour = date.getHours();
                    const dayOfWeek = date.getDay();
                    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
                    
                    let baseOccupancy = 0.3;
                    if (hour >= 8 && hour <= 10) baseOccupancy = 0.85;
                    else if (hour >= 12 && hour <= 14) baseOccupancy = 0.75;
                    else if (hour >= 17 && hour <= 19) baseOccupancy = 0.80;
                    else if (hour >= 22 || hour <= 6) baseOccupancy = 0.10;
                    
                    if (isWeekend) baseOccupancy *= 0.4;
                    
                    const variation = (Math.random() - 0.5) * 0.2;
                    const occupancyRate = Math.max(0, Math.min(1, baseOccupancy + variation));
                    
                    const occupied = Math.round(lot.capacity * occupancyRate);
                    const shadedOccupied = Math.round(lot.shaded_capacity * occupancyRate * 1.1);
                    
                    database.run(
                        'INSERT INTO occupancy (lot_id, occupied, shaded_occupied, timestamp) VALUES (?, ?, ?, ?)',
                        [lot.lot_id, occupied, shadedOccupied, new Date(time).toISOString()],
                        () => {} // Silent insert
                    );
                }
            });
            
            database.close((err) => {
                if (err) {
                    console.error('Error closing database:', err);
                    reject(err);
                } else {
                    console.log('✅ Database setup complete!');
                    console.log(`📁 Database location: ${dbPath}`);
                    resolve();
                }
            });
        });
    });
}

// Run setup
setupDatabase().catch(console.error);
