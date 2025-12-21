const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, 'parkurban.db');

// Initialize database connection
function getDB() {
    return new sqlite3.Database(DB_PATH, (err) => {
        if (err) {
            console.error('Error opening database:', err);
        }
    });
}

// Initialize database schema
function initializeDB() {
    const db = getDB();
    
    return new Promise((resolve, reject) => {
        db.serialize(() => {
            // Lots table
            db.run(`CREATE TABLE IF NOT EXISTS lots (
                lot_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                shaded_capacity INTEGER NOT NULL,
                latitude REAL,
                longitude REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )`);
            
            // Occupancy table (time-series data)
            db.run(`CREATE TABLE IF NOT EXISTS occupancy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id TEXT NOT NULL,
                occupied INTEGER NOT NULL,
                shaded_occupied INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES lots(lot_id)
            )`);
            
            // Create index for faster queries
            db.run(`CREATE INDEX IF NOT EXISTS idx_occupancy_lot_time 
                ON occupancy(lot_id, timestamp DESC)`);
            
            // EV Chargers table
            db.run(`CREATE TABLE IF NOT EXISTS ev_chargers (
                charger_id TEXT PRIMARY KEY,
                lot_id TEXT NOT NULL,
                name TEXT,
                status TEXT NOT NULL,
                power_kw REAL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES lots(lot_id)
            )`);
            
            // Forecasts table (cached predictions)
            db.run(`CREATE TABLE IF NOT EXISTS forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id TEXT NOT NULL,
                horizon_minutes INTEGER NOT NULL,
                predicted_open INTEGER NOT NULL,
                confidence REAL,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES lots(lot_id)
            )`);
            
            db.close((err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    });
}

// Database operations
const db = {
    // Lots
    async getAllLots() {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.all('SELECT * FROM lots ORDER BY name', (err, rows) => {
                db.close();
                if (err) reject(err);
                else resolve(rows);
            });
        });
    },
    
    async getLot(lot_id) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.get('SELECT * FROM lots WHERE lot_id = ?', [lot_id], (err, row) => {
                db.close();
                if (err) reject(err);
                else resolve(row);
            });
        });
    },
    
    // Occupancy
    async getLatestOccupancy(lot_id) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.get(
                'SELECT * FROM occupancy WHERE lot_id = ? ORDER BY timestamp DESC LIMIT 1',
                [lot_id],
                (err, row) => {
                    db.close();
                    if (err) reject(err);
                    else resolve(row);
                }
            );
        });
    },
    
    async insertOccupancy(lot_id, occupied, shaded_occupied) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.run(
                'INSERT INTO occupancy (lot_id, occupied, shaded_occupied) VALUES (?, ?, ?)',
                [lot_id, occupied, shaded_occupied],
                function(err) {
                    db.close();
                    if (err) reject(err);
                    else resolve(this.lastID);
                }
            );
        });
    },
    
    async getOccupancyHistory(lot_id, hours = 24) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            const cutoff = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
            db.all(
                `SELECT * FROM occupancy 
                 WHERE lot_id = ? AND timestamp >= ? 
                 ORDER BY timestamp ASC`,
                [lot_id, cutoff],
                (err, rows) => {
                    db.close();
                    if (err) reject(err);
                    else resolve(rows);
                }
            );
        });
    },
    
    // EV Chargers
    async getAllEVStatus() {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.all('SELECT * FROM ev_chargers ORDER BY lot_id, charger_id', (err, rows) => {
                db.close();
                if (err) reject(err);
                else resolve(rows);
            });
        });
    },
    
    async getEVStatusForLot(lot_id) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.all(
                'SELECT * FROM ev_chargers WHERE lot_id = ? ORDER BY charger_id',
                [lot_id],
                (err, rows) => {
                    db.close();
                    if (err) reject(err);
                    else resolve(rows);
                }
            );
        });
    },
    
    async updateEVStatus(charger_id, status) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.run(
                'UPDATE ev_chargers SET status = ?, last_updated = CURRENT_TIMESTAMP WHERE charger_id = ?',
                [status, charger_id],
                function(err) {
                    db.close();
                    if (err) reject(err);
                    else resolve(this.changes);
                }
            );
        });
    },
    
    async insertOrUpdateEVCharger(charger_id, lot_id, name, status, power_kw) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.run(
                `INSERT INTO ev_chargers (charger_id, lot_id, name, status, power_kw)
                 VALUES (?, ?, ?, ?, ?)
                 ON CONFLICT(charger_id) DO UPDATE SET
                 status = excluded.status,
                 last_updated = CURRENT_TIMESTAMP`,
                [charger_id, lot_id, name, status, power_kw],
                function(err) {
                    db.close();
                    if (err) reject(err);
                    else resolve(this.lastID);
                }
            );
        });
    },
    
    // Forecasts
    async saveForecast(lot_id, horizon_minutes, predicted_open, confidence) {
        return new Promise((resolve, reject) => {
            const db = getDB();
            db.run(
                `INSERT INTO forecasts (lot_id, horizon_minutes, predicted_open, confidence)
                 VALUES (?, ?, ?, ?)`,
                [lot_id, horizon_minutes, predicted_open, confidence],
                function(err) {
                    db.close();
                    if (err) reject(err);
                    else resolve(this.lastID);
                }
            );
        });
    }
};

// Initialize on module load
initializeDB().catch(console.error);

module.exports = db;
