import numpy as np
from sklearn.ensemble import RandomForestClassifier

class DiagnosisAgent:
    def __init__(self):
        self.name = "DiagnosisAgent"
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        X_train = np.random.randn(200, 4)
        y_train = np.random.randint(0, 2, 200)
        self.model.fit(X_train, y_train)
    
    def predict_failures(self, vehicle_id):
        features = np.array([[88, 3.2, 65, 75000]])
        failure_prob = self.model.predict_proba(features)[0][1]
        
        predictions = {
            "vehicle_id": vehicle_id,
            "failure_probability": round(failure_prob * 100, 1),
            "risk_level": "CRITICAL" if failure_prob > 0.8 else "HIGH" if failure_prob > 0.6 else "MEDIUM" if failure_prob > 0.4 else "LOW",
            "predicted_failures": [],
        }
        
        components = {
            "bearing": failure_prob * 0.85,
            "oil_pump": failure_prob * 0.45,
            "fuel_injector": failure_prob * 0.30,
        }
        
        for component, prob in components.items():
            if prob > 0.5:
                predictions["predicted_failures"].append({
                    "component": component,
                    "failure_probability": round(prob * 100, 1),
                })
        
        return predictions
