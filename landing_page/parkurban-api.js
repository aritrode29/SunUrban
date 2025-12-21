/**
 * ParkUrban API Client
 * Fetches real-time parking data from the backend API
 */

// API Configuration - Update this to your deployed backend URL
const API_CONFIG = {
    // For local development:
    baseURL: 'http://localhost:3000',
    
    // For production, update to your deployed backend:
    // baseURL: 'https://your-api.render.com',
    
    // Fallback to simulated data if API is unavailable
    useSimulatedData: false
};

class ParkUrbanAPI {
    constructor(config = API_CONFIG) {
        this.baseURL = config.baseURL;
        this.useSimulatedData = config.useSimulatedData;
    }

    async fetchLots() {
        try {
            const response = await fetch(`${this.baseURL}/api/lots`);
            if (!response.ok) throw new Error('API request failed');
            const data = await response.json();
            return data.lots;
        } catch (error) {
            console.warn('API fetch failed, using simulated data:', error);
            if (this.useSimulatedData) {
                return this.getSimulatedLots();
            }
            throw error;
        }
    }

    async fetchForecast(lot_id) {
        try {
            const response = await fetch(`${this.baseURL}/api/forecast?lot_id=${lot_id}`);
            if (!response.ok) throw new Error('Forecast request failed');
            return await response.json();
        } catch (error) {
            console.warn('Forecast fetch failed:', error);
            return this.getSimulatedForecast(lot_id);
        }
    }

    async fetchEVStatus(lot_id = null) {
        try {
            const url = lot_id 
                ? `${this.baseURL}/api/ev?lot_id=${lot_id}`
                : `${this.baseURL}/api/ev`;
            const response = await fetch(url);
            if (!response.ok) throw new Error('EV status request failed');
            return await response.json();
        } catch (error) {
            console.warn('EV status fetch failed:', error);
            return this.getSimulatedEVStatus(lot_id);
        }
    }

    // Simulated data fallback
    getSimulatedLots() {
        const now = new Date();
        const hour = now.getHours();
        const isWeekend = now.getDay() === 0 || now.getDay() === 6;
        
        let baseOccupancy = 0.3;
        if (hour >= 8 && hour <= 10) baseOccupancy = 0.85;
        else if (hour >= 12 && hour <= 14) baseOccupancy = 0.75;
        else if (hour >= 17 && hour <= 19) baseOccupancy = 0.80;
        else if (hour >= 22 || hour <= 6) baseOccupancy = 0.10;
        
        if (isWeekend) baseOccupancy *= 0.4;
        
        return [
            {
                lot_id: 'lot1',
                name: 'Lot 1 - Speedway',
                capacity: 450,
                shaded_capacity: 180,
                current_occupied: Math.round(450 * baseOccupancy),
                current_open: Math.round(450 * (1 - baseOccupancy)),
                occupancy_percent: (baseOccupancy * 100).toFixed(1),
                shaded_open: Math.round(180 * (1 - baseOccupancy * 1.1)),
                ev_available: 2,
                ev_total: 3,
                last_updated: new Date().toISOString()
            },
            {
                lot_id: 'lot2',
                name: 'Lot 2 - San Jacinto',
                capacity: 320,
                shaded_capacity: 128,
                current_occupied: Math.round(320 * baseOccupancy),
                current_open: Math.round(320 * (1 - baseOccupancy)),
                occupancy_percent: (baseOccupancy * 100).toFixed(1),
                shaded_open: Math.round(128 * (1 - baseOccupancy * 1.1)),
                ev_available: 1,
                ev_total: 2,
                last_updated: new Date().toISOString()
            },
            {
                lot_id: 'lot3',
                name: 'Lot 3 - East Campus',
                capacity: 280,
                shaded_capacity: 112,
                current_occupied: Math.round(280 * baseOccupancy),
                current_open: Math.round(280 * (1 - baseOccupancy)),
                occupancy_percent: (baseOccupancy * 100).toFixed(1),
                shaded_open: Math.round(112 * (1 - baseOccupancy * 1.1)),
                ev_available: 1,
                ev_total: 1,
                last_updated: new Date().toISOString()
            }
        ];
    }

    getSimulatedForecast(lot_id) {
        return {
            lot_id,
            forecasts: {
                '15': { predicted_open: 45, confidence: 0.75 },
                '30': { predicted_open: 52, confidence: 0.70 },
                '60': { predicted_open: 68, confidence: 0.65 }
            }
        };
    }

    getSimulatedEVStatus(lot_id) {
        return {
            chargers: [],
            summary: { total: 0, available: 0, in_use: 0, out_of_service: 0 }
        };
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ParkUrbanAPI;
}
