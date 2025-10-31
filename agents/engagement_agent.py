import json
from datetime import datetime
import random

class CustomerEngagementAgent:
    def __init__(self):
        self.name = "CustomerEngagementAgent"
        try:
            with open("data/synthetic_vehicles.json", "r") as f:
                self.vehicles = json.load(f)
        except:
            self.vehicles = []
    
    def get_vehicle_owner(self, vehicle_id):
        for v in self.vehicles:
            if v['vehicle_id'] == vehicle_id:
                return v
        return None
    
    def initiate_outreach(self, vehicle_id, diagnosis):
        vehicle = self.get_vehicle_owner(vehicle_id)
        if not vehicle:
            return {"error": "Vehicle not found"}
        
        risk_acceptance = {"MEDIUM": 0.7, "HIGH": 0.85, "CRITICAL": 0.95}
        risk = diagnosis.get('risk_level', 'LOW')
        acceptance_rate = risk_acceptance.get(risk, 0.5)
        customer_agreed = random.random() < acceptance_rate
        
        return {
            "vehicle_id": vehicle_id,
            "owner_name": vehicle['owner_name'],
            "phone": vehicle['phone_number'],
            "customer_agreed": customer_agreed,
            "timestamp": datetime.now().isoformat()
        }
