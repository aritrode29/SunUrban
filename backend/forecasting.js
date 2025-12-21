/**
 * Forecasting module for ParkUrban
 * Generates 15/30/60 minute predictions using baseline models
 */

function generateForecast(history, lot, horizonMinutes) {
    if (!history || history.length === 0) {
        // No history - return current capacity as baseline
        return {
            predicted_open: lot.capacity * 0.3, // Assume 30% available
            confidence: 0.3,
            method: 'baseline'
        };
    }
    
    const now = new Date();
    const targetTime = new Date(now.getTime() + horizonMinutes * 60 * 1000);
    const targetHour = targetTime.getHours();
    const targetDayOfWeek = targetTime.getDay();
    
    // Method 1: Last-week same time average (most reliable baseline)
    const lastWeekSameTime = getLastWeekAverage(history, targetHour, targetDayOfWeek);
    
    // Method 2: Recent trend (last hour average)
    const recentTrend = getRecentTrend(history, 60);
    
    // Method 3: Time-of-day pattern
    const timeOfDayPattern = getTimeOfDayPattern(history, targetHour);
    
    // Combine methods (weighted average)
    const weights = {
        lastWeek: 0.5,
        recentTrend: 0.3,
        timeOfDay: 0.2
    };
    
    const predictedOccupied = Math.round(
        lastWeekSameTime.occupied * weights.lastWeek +
        recentTrend.occupied * weights.recentTrend +
        timeOfDayPattern.occupied * weights.timeOfDay
    );
    
    const predictedOpen = Math.max(0, Math.min(lot.capacity, lot.capacity - predictedOccupied));
    
    // Calculate confidence based on data quality
    let confidence = 0.7; // Base confidence
    if (history.length < 10) confidence = 0.4; // Low data
    if (history.length > 100) confidence = 0.85; // High data
    
    // Lower confidence for longer horizons
    confidence *= (1 - horizonMinutes / 120); // Decrease confidence for longer predictions
    
    return {
        predicted_open: predictedOpen,
        predicted_occupied: predictedOccupied,
        confidence: Math.max(0.3, Math.min(0.9, confidence)),
        method: 'weighted_average',
        components: {
            last_week: lastWeekSameTime.occupied,
            recent_trend: recentTrend.occupied,
            time_of_day: timeOfDayPattern.occupied
        }
    };
}

function getLastWeekAverage(history, targetHour, targetDayOfWeek) {
    // Find data points from same day of week and similar hour (±1 hour)
    const relevant = history.filter(h => {
        const hDate = new Date(h.timestamp);
        const hDay = hDate.getDay();
        const hHour = hDate.getHours();
        return hDay === targetDayOfWeek && Math.abs(hHour - targetHour) <= 1;
    });
    
    if (relevant.length === 0) {
        // Fallback to overall average
        const avg = history.reduce((sum, h) => sum + h.occupied, 0) / history.length;
        return { occupied: avg, count: history.length };
    }
    
    const avg = relevant.reduce((sum, h) => sum + h.occupied, 0) / relevant.length;
    return { occupied: avg, count: relevant.length };
}

function getRecentTrend(history, minutes) {
    const cutoff = new Date(Date.now() - minutes * 60 * 1000);
    const recent = history.filter(h => new Date(h.timestamp) >= cutoff);
    
    if (recent.length === 0) {
        const latest = history[history.length - 1];
        return { occupied: latest?.occupied || 0, count: 0 };
    }
    
    // Use most recent value (or average of last few)
    const lastFew = recent.slice(-3);
    const avg = lastFew.reduce((sum, h) => sum + h.occupied, 0) / lastFew.length;
    return { occupied: avg, count: recent.length };
}

function getTimeOfDayPattern(history, targetHour) {
    // Find all data points at similar hours (±1 hour)
    const relevant = history.filter(h => {
        const hDate = new Date(h.timestamp);
        const hHour = hDate.getHours();
        return Math.abs(hHour - targetHour) <= 1;
    });
    
    if (relevant.length === 0) {
        const avg = history.reduce((sum, h) => sum + h.occupied, 0) / history.length;
        return { occupied: avg, count: history.length };
    }
    
    const avg = relevant.reduce((sum, h) => sum + h.occupied, 0) / relevant.length;
    return { occupied: avg, count: relevant.length };
}

module.exports = { generateForecast };
