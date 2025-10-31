import json
import random
import time
from datetime import datetime, timedelta
import threading
import os

class RealtimeSimulator:
    """Simulates real-time vehicle telemetry data"""
    
    def __init__(self):
        self.vehicles = {
            "VH1001": {
                "owner": "Owner 1",
                "model": "Hero Splendor",
                "location": "Delhi",
                "base_temp": 85,
                "base_pressure": 4.5
            },
            "VH1002": {
                "owner": "Owner 2",
                "model": "Mahindra XUV500",
                "location": "Mumbai",
                "base_temp": 82,
                "base_pressure": 4.3
            },
            "VH1003": {
                "owner": "Owner 3",
                "model": "Hero Apache",
                "location": "Bangalore",
                "base_temp": 88,
                "base_pressure": 4.6
            }
        }
        
        self.data_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 'data', 'telemetry_stream.json'
        )
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def generate_telemetry(self, vehicle_id, degradation_factor=0.5):
        """Generate realistic telemetry data with degradation"""
        vehicle = self.vehicles.get(vehicle_id, {})
        
        # Simulate degradation over time
        base_temp = vehicle.get('base_temp', 85)
        base_pressure = vehicle.get('base_pressure', 4.5)
        
        # Add noise and degradation
        engine_temp = base_temp + random.gauss(5, 3) + (degradation_factor * 10)
        oil_pressure = base_pressure + random.gauss(0, 0.3) - (degradation_factor * 0.5)
        rpm = 2500 + random.gauss(500, 200)
        fuel_consumption = 12 + random.gauss(-2, 1)
        sensor_health = max(0, 100 - (degradation_factor * 50))
        battery_voltage = 12.6 + random.gauss(0.2, 0.1)
        
        # Determine alert status
        alert = "NORMAL"
        if sensor_health < 60:
            alert = "WARNING"
        if sensor_health < 40:
            alert = "CRITICAL"
        
        return {
            "vehicle_id": vehicle_id,
            "timestamp": datetime.now().isoformat(),
            "engine_temp_celsius": round(engine_temp, 2),
            "oil_pressure_bar": round(oil_pressure, 2),
            "rpm": round(rpm, 0),
            "fuel_consumption_kmpl": round(fuel_consumption, 2),
            "battery_voltage": round(battery_voltage, 2),
            "tire_pressure_psi": [round(32 + random.gauss(0, 1), 2) for _ in range(4)],
            "sensor_health": round(sensor_health, 2),
            "location": self.vehicles[vehicle_id].get('location'),
            "alert_status": alert,
            "degradation_factor": round(degradation_factor, 2)
        }
    
    def stream_telemetry(self, duration_seconds=3600, interval=5):
        """Continuously stream telemetry data"""
        start_time = time.time()
        step = 0
        
        print("🔴 Starting real-time telemetry stream...")
        
        while (time.time() - start_time) < duration_seconds:
            try:
                stream_data = []
                
                # Generate data for all vehicles
                for vehicle_id in self.vehicles.keys():
                    # VH1001 degrades faster (bearing issue)
                    if vehicle_id == "VH1001":
                        degradation = (step / 200) * 0.8  # Fast degradation
                    else:
                        degradation = (step / 500) * 0.3  # Slow degradation
                    
                    telemetry = self.generate_telemetry(vehicle_id, degradation)
                    stream_data.append(telemetry)
                
                # Save to file (Streamlit will read this)
                with open(self.data_file, 'w') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "vehicles": stream_data,
                        "update_count": step
                    }, f, indent=2)
                
                print(f"  📊 Update {step}: Generated data for {len(stream_data)} vehicles")
                
                time.sleep(interval)
                step += 1
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                time.sleep(interval)
    
    def start_background_stream(self):
        """Start streaming in background thread"""
        thread = threading.Thread(target=self.stream_telemetry, daemon=True)
        thread.start()
        print("✓ Background telemetry stream started")
        return thread

# For standalone testing
if __name__ == "__main__":
    simulator = RealtimeSimulator()
    simulator.stream_telemetry(duration_seconds=300, interval=5)  # Run for 5 minutes
