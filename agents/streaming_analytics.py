import json
from datetime import datetime, timedelta
import random

class StreamingAnalytics:
    def __init__(self):
        self.name = "StreamingAnalytics"
    
    def get_live_fleet_status(self):
        """Real-time fleet health snapshot"""
        vehicles = ["VH1001", "VH1002", "VH1003", "VH1004", "VH1005"]
        status = []
        
        for vehicle_id in vehicles:
            status.append({
                "vehicle_id": vehicle_id,
                "timestamp": datetime.now().isoformat(),
                "engine_temp": round(85 + random.gauss(5, 3), 1),
                "oil_pressure": round(4.5 + random.gauss(0, 0.3), 1),
                "rpm": round(2500 + random.gauss(500, 200), 0),
                "alert": "CRITICAL" if random.random() > 0.8 else "NORMAL"
            })
        
        return status
    
    def get_predictive_alerts(self):
        """High-priority alerts that need immediate attention"""
        return [
            {
                "alert_id": "ALT_001",
                "vehicle_id": "VH1001",
                "severity": "CRITICAL",
                "message": "Bearing failure predicted in 3 days",
                "recommended_action": "Schedule maintenance immediately",
                "confidence": 89
            },
            {
                "alert_id": "ALT_002",
                "vehicle_id": "VH1003",
                "severity": "HIGH",
                "message": "Oil pressure declining - sensor issue likely",
                "recommended_action": "Check sensor calibration",
                "confidence": 76
            }
        ]
    
    def get_fleet_optimization(self):
        """AI-powered fleet optimization recommendations"""
        return {
            "total_vehicles": 10,
            "healthy": 6,
            "maintenance_needed": 3,
            "critical": 1,
            "cost_optimization": {
                "current_cost_per_vehicle_per_year": 45000,
                "predicted_cost_with_system": 27000,
                "savings_percentage": 40
            },
            "recommendations": [
                "Schedule VH1001 maintenance before critical failure",
                "VH1005 battery needs replacement within 2 weeks",
                "Service center SC_2 has high capacity - use for scheduling"
            ]
        }
