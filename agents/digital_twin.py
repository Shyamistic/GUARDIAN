import json
import numpy as np
from datetime import datetime, timedelta

class DigitalTwin:
    """Creates digital twin of vehicle for predictive simulation"""
    
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.state = {
            "engine_temp": 85,
            "oil_pressure": 4.5,
            "bearing_wear": 0.1,
            "sensor_health": 100,
            "mileage": 75000
        }
        
    def simulate_future_states(self, days=30):
        """Simulate vehicle state N days into future"""
        
        future_states = []
        current_state = self.state.copy()
        
        for day in range(days):
            # Simulate degradation
            current_state['bearing_wear'] += 0.02 * (1 + day/100)
            current_state['sensor_health'] -= 1.5 * (1 + current_state['bearing_wear'])
            current_state['engine_temp'] += 0.5 * current_state['bearing_wear']
            current_state['oil_pressure'] -= 0.01 * current_state['bearing_wear']
            current_state['mileage'] += 50
            
            # Predict failure point
            failure_risk = 0
            if current_state['bearing_wear'] > 0.8:
                failure_risk = 90
            elif current_state['bearing_wear'] > 0.6:
                failure_risk = 70
            elif current_state['bearing_wear'] > 0.4:
                failure_risk = 40
            
            future_states.append({
                "day": day + 1,
                "date": (datetime.now() + timedelta(days=day+1)).strftime("%Y-%m-%d"),
                "state": current_state.copy(),
                "failure_risk": failure_risk,
                "recommendation": "CRITICAL MAINTENANCE" if failure_risk > 80 else "SCHEDULE SOON" if failure_risk > 50 else "MONITOR"
            })
        
        return future_states
    
    def find_optimal_maintenance_window(self, future_states):
        """Find optimal time to schedule maintenance"""
        
        for state in future_states:
            if state['failure_risk'] > 70:
                return {
                    "optimal_day": state['day'],
                    "optimal_date": state['date'],
                    "reason": f"Failure risk reaches {state['failure_risk']}%",
                    "cost_if_delayed": 75000,
                    "cost_if_proactive": 28000,
                    "savings": 47000
                }
        
        return {
            "optimal_day": 30,
            "optimal_date": future_states[-1]['date'],
            "reason": "Routine maintenance window",
            "cost_if_delayed": 45000,
            "cost_if_proactive": 28000,
            "savings": 17000
        }
    
    def generate_twin_report(self):
        """Generate complete digital twin analysis"""
        
        future_states = self.simulate_future_states(30)
        optimal_window = self.find_optimal_maintenance_window(future_states)
        
        return {
            "vehicle_id": self.vehicle_id,
            "current_state": self.state,
            "30_day_forecast": future_states,
            "optimal_maintenance": optimal_window,
            "digital_twin_confidence": 89,
            "generated_at": datetime.now().isoformat()
        }

if __name__ == "__main__":
    twin = DigitalTwin("VH1001")
    report = twin.generate_twin_report()
    print(f"Optimal maintenance day: {report['optimal_maintenance']['optimal_day']}")
    print(f"Potential savings: ₹{report['optimal_maintenance']['savings']:,}")
