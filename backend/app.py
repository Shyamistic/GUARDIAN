from flask import Flask, jsonify, request
from flask_cors import CORS
from agents.guardian_crew import run_guardian_crew
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ============= HEALTH CHECK =============
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "service": "GUARDIAN Backend",
        "status": "OK",
        "timestamp": "2025-10-31T12:05:38.765719",
        "version": "2.0.0-agentic",
        "architecture": "Multi-Agent CrewAI System"
    }), 200

# ============= AUTONOMOUS CREW ENDPOINT =============
@app.route('/api/crew/diagnose', methods=['POST'])
def diagnose_vehicle():
    """Trigger the autonomous GUARDIAN crew for a vehicle."""
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id', 'VH1001')
        sensor_data = data.get('sensor_data', {
            'engine_temp_celsius': 95,
            'oil_pressure_bar': 3.2,
            'sensor_health': 65,
            'rpm': 4500,
            'degradation_factor': 0.78
        })
        
        # RUN THE AUTONOMOUS CREW
        result = run_guardian_crew(vehicle_id, sensor_data)
        
        return jsonify({
            "status": "success",
            "data": result,
            "message": "Autonomous crew decision completed"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ============= VEHICLES ENDPOINT =============
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """Get list of all vehicles in the fleet"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "vehicle_id": "VH1001",
                "make": "Tata",
                "model": "1613",
                "year": 2022,
                "health_status": "Critical",
                "engine_temp": 105,
                "oil_pressure": 2.2,
                "sensor_health": 60,
                "last_check": "2025-10-31T14:30:00Z",
                "alert_level": "high",
                "predicted_failure": "Bearing failure",
                "days_to_failure": "3-5",
                "confidence": 89
            },
            {
                "vehicle_id": "VH1002",
                "make": "Ashok Leyland",
                "model": "2516",
                "year": 2023,
                "health_status": "Healthy",
                "engine_temp": 85,
                "oil_pressure": 3.5,
                "sensor_health": 92,
                "last_check": "2025-10-31T14:35:00Z",
                "alert_level": "none",
                "predicted_failure": null,
                "days_to_failure": null,
                "confidence": null
            },
            {
                "vehicle_id": "VH1003",
                "make": "Bharat Benz",
                "model": "1617R",
                "year": 2023,
                "health_status": "Warning",
                "engine_temp": 95,
                "oil_pressure": 3.0,
                "sensor_health": 75,
                "last_check": "2025-10-31T14:28:00Z",
                "alert_level": "medium",
                "predicted_failure": "Oil system degradation",
                "days_to_failure": "7-10",
                "confidence": 76
            },
            {
                "vehicle_id": "VH1004",
                "make": "Tata",
                "model": "LPT 1918",
                "year": 2021,
                "health_status": "Healthy",
                "engine_temp": 82,
                "oil_pressure": 3.8,
                "sensor_health": 88,
                "last_check": "2025-10-31T14:20:00Z",
                "alert_level": "none",
                "predicted_failure": null,
                "days_to_failure": null,
                "confidence": null
            },
            {
                "vehicle_id": "VH1005",
                "make": "Mahindra",
                "model": "Blazo X 35",
                "year": 2024,
                "health_status": "Warning",
                "engine_temp": 98,
                "oil_pressure": 2.9,
                "sensor_health": 70,
                "last_check": "2025-10-31T14:25:00Z",
                "alert_level": "medium",
                "predicted_failure": "Cooling system issue",
                "days_to_failure": "10-14",
                "confidence": 68
            }
        ]
    }), 200

# ============= INDIVIDUAL VEHICLE ENDPOINT =============
@app.route('/api/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle_detail(vehicle_id):
    """Get detailed information for a specific vehicle"""
    # Mock data for demo
    vehicles = {
        "VH1001": {
            "vehicle_id": "VH1001",
            "make": "Tata",
            "model": "1613",
            "year": 2022,
            "health_status": "Critical",
            "sensor_data": {
                "engine_temp": 105,
                "oil_pressure": 2.2,
                "sensor_health": 60,
                "rpm": 5000,
                "fuel_level": 45,
                "battery_voltage": 12.2
            },
            "last_check": "2025-10-31T14:30:00Z",
            "alert_level": "high",
            "predicted_failure": "Bearing failure",
            "days_to_failure": "3-5",
            "confidence": 89,
            "maintenance_history": [
                {"date": "2025-10-15", "type": "Oil Change", "cost": 3500},
                {"date": "2025-09-01", "type": "Brake Inspection", "cost": 5000},
                {"date": "2025-07-20", "type": "Tire Rotation", "cost": 2000}
            ]
        }
    }
    
    vehicle = vehicles.get(vehicle_id, vehicles["VH1001"])
    return jsonify({
        "status": "success",
        "data": vehicle
    }), 200

# ============= WORKFLOWS ENDPOINT =============
@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Get workflow execution history"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "workflow_id": "WF_001",
                "vehicle_id": "VH1001",
                "timestamp": "2025-10-31T14:30:00Z",
                "agents_involved": ["Diagnostic Specialist", "Customer Engagement", "ROI Analyst", "Master Orchestrator"],
                "status": "completed",
                "decision": "Schedule urgent maintenance - Bearing failure predicted",
                "estimated_savings": 35000,
                "execution_time_seconds": 12.5,
                "confidence": 89
            },
            {
                "workflow_id": "WF_002",
                "vehicle_id": "VH1003",
                "timestamp": "2025-10-31T12:15:00Z",
                "agents_involved": ["Diagnostic Specialist", "ROI Analyst", "Master Orchestrator"],
                "status": "completed",
                "decision": "Monitor for 48 hours - Oil system showing early degradation",
                "estimated_savings": 15000,
                "execution_time_seconds": 8.3,
                "confidence": 76
            },
            {
                "workflow_id": "WF_003",
                "vehicle_id": "VH1005",
                "timestamp": "2025-10-31T10:45:00Z",
                "agents_involved": ["Diagnostic Specialist", "Customer Engagement", "ROI Analyst"],
                "status": "completed",
                "decision": "Schedule maintenance within 2 weeks - Cooling system needs attention",
                "estimated_savings": 22000,
                "execution_time_seconds": 10.1,
                "confidence": 68
            },
            {
                "workflow_id": "WF_004",
                "vehicle_id": "VH1002",
                "timestamp": "2025-10-31T09:30:00Z",
                "agents_involved": ["Diagnostic Specialist"],
                "status": "completed",
                "decision": "All systems healthy - Continue regular monitoring",
                "estimated_savings": 0,
                "execution_time_seconds": 4.2,
                "confidence": 95
            }
        ]
    }), 200

# ============= ALERTS ENDPOINT =============
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get predictive alerts"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "alert_id": "ALR_001",
                "vehicle_id": "VH1001",
                "severity": "critical",
                "predicted_failure": "Bearing failure",
                "confidence": 89,
                "days_to_failure": "3-5",
                "recommended_action": "Immediate service required - Schedule within 24 hours",
                "estimated_cost_if_ignored": 50000,
                "preventive_cost": 15000,
                "potential_savings": 35000,
                "timestamp": "2025-10-31T14:30:00Z",
                "acknowledged": False
            },
            {
                "alert_id": "ALR_002",
                "vehicle_id": "VH1003",
                "severity": "warning",
                "predicted_failure": "Oil system degradation",
                "confidence": 76,
                "days_to_failure": "7-10",
                "recommended_action": "Schedule maintenance within a week",
                "estimated_cost_if_ignored": 35000,
                "preventive_cost": 12000,
                "potential_savings": 23000,
                "timestamp": "2025-10-31T12:15:00Z",
                "acknowledged": False
            },
            {
                "alert_id": "ALR_003",
                "vehicle_id": "VH1005",
                "severity": "warning",
                "predicted_failure": "Cooling system issue",
                "confidence": 68,
                "days_to_failure": "10-14",
                "recommended_action": "Schedule maintenance within 2 weeks",
                "estimated_cost_if_ignored": 40000,
                "preventive_cost": 18000,
                "potential_savings": 22000,
                "timestamp": "2025-10-31T10:45:00Z",
                "acknowledged": True
            }
        ]
    }), 200

# ============= ANALYTICS ENDPOINT =============
@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Get fleet analytics and KPIs"""
    return jsonify({
        "status": "success",
        "data": {
            "total_vehicles": 5,
            "healthy_vehicles": 2,
            "warning_vehicles": 2,
            "critical_vehicles": 1,
            "total_predictions": 47,
            "total_alerts": 12,
            "autonomous_decisions": 8,
            "crew_interventions": 4,
            "total_estimated_savings": 95000,
            "avg_prediction_confidence": 81,
            "uptime_percentage": 94.5,
            "maintenance_scheduled": 3,
            "maintenance_completed": 15
        }
    }), 200

# ============= HEALTH HISTORY ENDPOINT =============
@app.route('/api/vehicles/<vehicle_id>/history', methods=['GET'])
def get_vehicle_history(vehicle_id):
    """Get historical sensor data for a vehicle"""
    return jsonify({
        "status": "success",
        "data": {
            "vehicle_id": vehicle_id,
            "history": [
                {"timestamp": "2025-10-31T14:00:00Z", "engine_temp": 103, "oil_pressure": 2.3, "sensor_health": 62},
                {"timestamp": "2025-10-31T12:00:00Z", "engine_temp": 98, "oil_pressure": 2.5, "sensor_health": 65},
                {"timestamp": "2025-10-31T10:00:00Z", "engine_temp": 92, "oil_pressure": 2.8, "sensor_health": 68},
                {"timestamp": "2025-10-31T08:00:00Z", "engine_temp": 88, "oil_pressure": 3.0, "sensor_health": 70},
                {"timestamp": "2025-10-31T06:00:00Z", "engine_temp": 85, "oil_pressure": 3.2, "sensor_health": 72}
            ]
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
