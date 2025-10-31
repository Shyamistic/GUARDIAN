import json
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

class DataAnalysisAgent:
    def __init__(self):
        self.name = "DataAnalysisAgent"
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        print(f"✓ {self.name} initialized")
        
    def load_vehicle_data(self, vehicle_id):
        try:
            with open("data/synthetic_vehicles.json", "r") as f:
                vehicles = json.load(f)
            for v in vehicles:
                if v['vehicle_id'] == vehicle_id:
                    return v
        except Exception as e:
            print(f"Error loading vehicle data: {e}")
        return None
    
    def load_telemetry(self, vehicle_id, num_readings=100):
        data = []
        base_temp = 85
        
        for i in range(num_readings):
            degradation = 1 + (i / num_readings) * 0.3
            data.append({
                "engine_temp": base_temp + np.random.normal(5, 3) * degradation,
                "oil_pressure": 4.5 + np.random.normal(0, 0.3) - (degradation * 0.3),
                "rpm": 2500 + np.random.normal(500, 200),
                "sensor_health": max(0, 100 - (i / num_readings * 40))
            })
        
        return pd.DataFrame(data)
    
    def detect_anomalies(self, vehicle_id):
        df = self.load_telemetry(vehicle_id)
        
        features = ['engine_temp', 'oil_pressure', 'rpm', 'sensor_health']
        X = df[features].values
        
        anomalies = self.isolation_forest.fit_predict(X)
        anomaly_scores = self.isolation_forest.score_samples(X)
        
        df['anomaly'] = anomalies
        df['anomaly_score'] = anomaly_scores
        
        anomalous_readings = df[df['anomaly'] == -1]
        
        return {
            "vehicle_id": vehicle_id,
            "total_readings": len(df),
            "anomalies_detected": len(anomalous_readings),
            "anomaly_readings": anomalous_readings.to_dict('records')
        }
    
    def forecast_service_demand(self, region=None):
        try:
            with open("data/maintenance_history.json", "r") as f:
                maintenance = json.load(f)
            
            df = pd.DataFrame(maintenance)
            
            if region:
                df = df[df['service_center'] == region]
            
            demand = df.groupby('repair_type').size().to_dict()
            
            return {
                "region": region or "All",
                "forecasted_services": demand,
                "total_predicted": sum(demand.values()),
                "average_cost": round(df['cost_inr'].mean(), 2) if len(df) > 0 else 0
            }
        except Exception as e:
            print(f"Error in forecast: {e}")
            return {"error": "Data not found"}
    
    def generate_health_report(self, vehicle_id):
        vehicle = self.load_vehicle_data(vehicle_id)
        anomalies = self.detect_anomalies(vehicle_id)
        demand = self.forecast_service_demand()
        
        num_anomalies = anomalies.get('anomalies_detected', 0)
        health_score = max(0, 100 - num_anomalies * 15)
        
        report = {
            "vehicle_id": vehicle_id,
            "vehicle_model": vehicle['model'] if vehicle else "Unknown",
            "health_score": health_score,
            "risk_level": "CRITICAL" if health_score < 40 else "HIGH" if health_score < 60 else "MEDIUM" if health_score < 80 else "LOW",
            "anomalies_detected": num_anomalies,
            "timestamp": datetime.now().isoformat(),
            "recommendation": "Schedule immediate service" if health_score < 60 else "Schedule routine maintenance"
        }
        
        return report
