import random
from datetime import datetime, timedelta

class SchedulingAgent:
    def __init__(self):
        self.name = "SchedulingAgent"
    
    def schedule_appointment(self, vehicle_id, center_id=None):
        base_date = datetime.now() + timedelta(days=1)
        selected_date = (base_date + timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        selected_time = f"{random.choice([9, 11, 14, 16]):02d}:00"
        
        return {
            "appointment_id": f"APT_{datetime.now().timestamp()}",
            "vehicle_id": vehicle_id,
            "service_center": center_id or "SC_1",
            "date": selected_date,
            "time": selected_time,
            "status": "CONFIRMED",
        }
