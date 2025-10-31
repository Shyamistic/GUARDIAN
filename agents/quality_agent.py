import json
from datetime import datetime

class ManufacturingQualityAgent:
    def __init__(self):
        self.name = "ManufacturingQualityAgent"
        try:
            with open("data/capa_records.json", "r") as f:
                self.capa_records = json.load(f)
        except:
            self.capa_records = []
    
    def analyze_failure_patterns(self, vehicle_id):
        insights = {
            "vehicle_id": vehicle_id,
            "timestamp": datetime.now().isoformat(),
            "recommendations": [],
            "capa_matches": []
        }
        
        for capa in self.capa_records:
            if capa['status'] in ['Implemented', 'In Progress']:
                insights['capa_matches'].append({
                    "capa_id": capa['capa_id'],
                    "defect": capa['defect_name'],
                })
        
        return insights
