import json
import os
from datetime import datetime

class Database:
    def __init__(self, filepath="data/guardian_db.json"):
        self.filepath = filepath
        self.ensure_exists()
    
    def ensure_exists(self):
        """Create database if it doesn't exist"""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self.reset()
    
    def reset(self):
        """Reset database to initial state"""
        initial = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "vehicles": [],
            "workflows": [],
            "alerts": [],
            "appointments": [],
            "predictions": [],
            "analytics": {
                "total_predictions": 0,
                "total_alerts": 0,
                "total_appointments": 0,
                "cost_savings": 0,
                "uptime_improvement": 6.2
            }
        }
        self.write(initial)
    
    def read(self):
        """Read entire database"""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def write(self, data):
        """Write entire database"""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing database: {e}")
            return False
    
    def add_vehicle(self, vehicle):
        """Add vehicle to database"""
        db = self.read()
        db['vehicles'].append(vehicle)
        self.write(db)
    
    def add_workflow(self, workflow):
        """Add workflow execution"""
        db = self.read()
        db['workflows'].append(workflow)
        db['analytics']['total_predictions'] += 1
        self.write(db)
    
    def add_alert(self, alert):
        """Add alert"""
        db = self.read()
        db['alerts'].append(alert)
        db['analytics']['total_alerts'] += 1
        self.write(db)
    
    def get_vehicle(self, vehicle_id):
        """Get specific vehicle"""
        db = self.read()
        return next((v for v in db['vehicles'] if v['vehicle_id'] == vehicle_id), None)
    
    def get_all_vehicles(self):
        """Get all vehicles"""
        db = self.read()
        return db.get('vehicles', [])
    
    def get_alerts(self, severity=None):
        """Get alerts"""
        db = self.read()
        alerts = db.get('alerts', [])
        if severity:
            return [a for a in alerts if a['severity'] == severity]
        return alerts
