from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging
import threading
import random
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# ============= DATA STORAGE =============
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "guardian_db.json")

# ============= REAL-TIME SIMULATOR =============
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

        self.data_file = os.path.join(DATA_DIR, "telemetry_stream.json")
        self.step = 0

    def generate_telemetry(self, vehicle_id, degradation_factor=0.5):
        """Generate realistic telemetry data with degradation"""
        vehicle = self.vehicles.get(vehicle_id, {})

        base_temp = vehicle.get('base_temp', 85)
        base_pressure = vehicle.get('base_pressure', 4.5)

        engine_temp = base_temp + random.gauss(5, 3) + (degradation_factor * 10)
        oil_pressure = base_pressure + random.gauss(0, 0.3) - (degradation_factor * 0.5)
        rpm = 2500 + random.gauss(500, 200)
        fuel_consumption = 12 + random.gauss(-2, 1)
        sensor_health = max(0, 100 - (degradation_factor * 50))
        battery_voltage = 12.6 + random.gauss(0.2, 0.1)

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

        logger.info("🔴 Starting real-time telemetry stream...")

        while (time.time() - start_time) < duration_seconds:
            try:
                stream_data = []

                for vehicle_id in self.vehicles.keys():
                    if vehicle_id == "VH1001":
                        degradation = (step / 200) * 0.8
                    else:
                        degradation = (step / 500) * 0.3

                    telemetry = self.generate_telemetry(vehicle_id, degradation)
                    stream_data.append(telemetry)

                with open(self.data_file, 'w') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "vehicles": stream_data,
                        "update_count": step
                    }, f, indent=2)

                logger.info(f"📊 Telemetry update {step}: {len(stream_data)} vehicles")

                time.sleep(interval)
                step += 1

            except Exception as e:
                logger.error(f"❌ Stream error: {e}")
                time.sleep(interval)

    def start_background_stream(self):
        """Start streaming in background thread"""
        thread = threading.Thread(target=self.stream_telemetry, daemon=True)
        thread.start()
        logger.info("✓ Background telemetry stream started")
        return thread

# Initialize simulator
simulator = RealtimeSimulator()

# ============= DATABASE FUNCTIONS =============
def ensure_db_exists():
    """Create database file if it doesn't exist"""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    if not os.path.exists(DB_FILE):
        initial_data = {
            "vehicles": [
                {
                    "vehicle_id": "VH1001",
                    "owner_name": "Owner 1",
                    "model": "Hero Splendor",
                    "health_score": 72,
                    "risk_level": "MEDIUM",
                    "created_at": datetime.now().isoformat(),
                    "last_analyzed": datetime.now().isoformat()
                },
                {
                    "vehicle_id": "VH1002",
                    "owner_name": "Owner 2",
                    "model": "Mahindra XUV500",
                    "health_score": 85,
                    "risk_level": "LOW",
                    "created_at": datetime.now().isoformat(),
                    "last_analyzed": datetime.now().isoformat()
                },
                {
                    "vehicle_id": "VH1003",
                    "owner_name": "Owner 3",
                    "model": "Hero Apache",
                    "health_score": 45,
                    "risk_level": "HIGH",
                    "created_at": datetime.now().isoformat(),
                    "last_analyzed": datetime.now().isoformat()
                }
            ],
            "workflows": [],
            "alerts": [
                {
                    "alert_id": "ALT_001",
                    "vehicle_id": "VH1001",
                    "severity": "CRITICAL",
                    "message": "Bearing failure predicted in 3 days",
                    "created_at": datetime.now().isoformat(),
                    "acknowledged": False
                },
                {
                    "alert_id": "ALT_002",
                    "vehicle_id": "VH1003",
                    "severity": "HIGH",
                    "message": "Oil pressure declining - sensor issue",
                    "created_at": datetime.now().isoformat(),
                    "acknowledged": False
                }
            ],
            "appointments": [],
            "analytics": {
                "total_predictions": 47,
                "total_alerts": 12,
                "total_appointments": 8,
                "cost_savings": 2450000
            }
        }
        with open(DB_FILE, "w") as f:
            json.dump(initial_data, f, indent=2)
        logger.info(f"✓ Database created at {DB_FILE}")

def load_db():
    """Load database"""
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading database: {e}")
        return {}

def save_db(data):
    """Save database"""
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving database: {e}")
        return False

# ============= HEALTH CHECK =============
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "GUARDIAN Backend"
    }), 200

# ============= VEHICLE ENDPOINTS =============
@app.route('/api/vehicles', methods=['GET'])
def get_all_vehicles():
    """Get all vehicles"""
    try:
        db = load_db()
        vehicles = db.get('vehicles', [])
        return jsonify({
            "status": "success",
            "count": len(vehicles),
            "data": vehicles
        }), 200
    except Exception as e:
        logger.error(f"Error getting vehicles: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get specific vehicle"""
    try:
        db = load_db()
        vehicles = db.get('vehicles', [])
        vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)

        if vehicle:
            return jsonify({"status": "success", "data": vehicle}), 200
        else:
            return jsonify({"status": "error", "message": "Vehicle not found"}), 404
    except Exception as e:
        logger.error(f"Error getting vehicle: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    """Create new vehicle"""
    try:
        data = request.json
        db = load_db()

        vehicle = {
            "vehicle_id": data.get('vehicle_id'),
            "owner_name": data.get('owner_name'),
            "model": data.get('model'),
            "health_score": 100,
            "risk_level": "LOW",
            "created_at": datetime.now().isoformat(),
            "last_analyzed": None
        }

        db['vehicles'].append(vehicle)
        save_db(db)

        return jsonify({"status": "success", "data": vehicle}), 201
    except Exception as e:
        logger.error(f"Error creating vehicle: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============= TELEMETRY ENDPOINTS =============
@app.route('/api/telemetry/stream', methods=['GET'])
def get_telemetry_stream():
    """Get real-time telemetry stream"""
    try:
        telemetry_file = os.path.join(DATA_DIR, "telemetry_stream.json")

        if os.path.exists(telemetry_file):
            with open(telemetry_file, 'r') as f:
                data = json.load(f)
            return jsonify({
                "status": "success",
                "data": data
            }), 200
        else:
            return jsonify({
                "status": "success",
                "data": {
                    "timestamp": datetime.now().isoformat(),
                    "vehicles": [],
                    "update_count": 0
                }
            }), 200
    except Exception as e:
        logger.error(f"Error getting telemetry stream: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/telemetry/vehicle/<vehicle_id>', methods=['GET'])
def get_vehicle_telemetry(vehicle_id):
    """Get latest telemetry for specific vehicle"""
    try:
        telemetry_file = os.path.join(DATA_DIR, "telemetry_stream.json")

        if os.path.exists(telemetry_file):
            with open(telemetry_file, 'r') as f:
                data = json.load(f)

            vehicles = data.get('vehicles', [])
            vehicle_data = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)

            if vehicle_data:
                return jsonify({
                    "status": "success",
                    "data": vehicle_data
                }), 200

        return jsonify({
            "status": "error",
            "message": "Vehicle data not found"
        }), 404
    except Exception as e:
        logger.error(f"Error getting vehicle telemetry: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============= PREDICTION ENDPOINTS =============
@app.route('/api/predict/<vehicle_id>', methods=['POST'])
def predict_failure(vehicle_id):
    """Get failure prediction for vehicle"""
    try:
        prediction = {
            "vehicle_id": vehicle_id,
            "failure_probability": round(random.uniform(40, 90), 1),
            "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "predicted_failures": [
                {"component": "bearing", "failure_probability": round(random.uniform(50, 90), 1)},
                {"component": "oil_pump", "failure_probability": round(random.uniform(30, 70), 1)}
            ]
        }

        db = load_db()
        db['analytics']['total_predictions'] += 1
        save_db(db)

        return jsonify({
            "status": "success",
            "data": prediction,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error predicting failure: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============= WORKFLOW ENDPOINTS =============
@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Get all workflows"""
    try:
        db = load_db()
        workflows = db.get('workflows', [])
        return jsonify({
            "status": "success",
            "count": len(workflows),
            "data": workflows
        }), 200
    except Exception as e:
        logger.error(f"Error getting workflows: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/workflows', methods=['POST'])
def create_workflow():
    """Create new workflow"""
    try:
        data = request.json
        db = load_db()

        workflow = {
            "workflow_id": f"WF_{datetime.now().timestamp()}",
            "vehicle_id": data.get('vehicle_id'),
            "status": "COMPLETED",
            "steps": data.get('steps', []),
            "created_at": datetime.now().isoformat()
        }

        db['workflows'].append(workflow)
        db['analytics']['total_predictions'] += 1
        save_db(db)

        return jsonify({"status": "success", "data": workflow}), 201
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============= ALERT ENDPOINTS =============
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get critical alerts"""
    try:
        db = load_db()
        alerts = db.get('alerts', [])

        severity = request.args.get('severity')
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]

        return jsonify({
            "status": "success",
            "count": len(alerts),
            "data": alerts
        }), 200
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create new alert"""
    try:
        data = request.json
        db = load_db()

        alert = {
            "alert_id": f"ALT_{datetime.now().timestamp()}",
            "vehicle_id": data.get('vehicle_id'),
            "severity": data.get('severity'),
            "message": data.get('message'),
            "created_at": datetime.now().isoformat(),
            "acknowledged": False
        }

        db['alerts'].append(alert)
        db['analytics']['total_alerts'] += 1
        save_db(db)

        return jsonify({"status": "success", "data": alert}), 201
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============= ANALYTICS ENDPOINTS =============
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get system analytics"""
    try:
        db = load_db()
        analytics = db.get('analytics', {})

        return jsonify({
            "status": "success",
            "data": {
                "total_predictions": analytics.get('total_predictions', 0),
                "total_alerts": analytics.get('total_alerts', 0),
                "total_appointments": analytics.get('total_appointments', 0),
                "total_cost_savings": analytics.get('cost_savings', 0),
                "uptime_improvement": "6.2%",
                "timestamp": datetime.now().isoformat()
            }
        }), 200
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ============= ERROR HANDLERS =============
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

# ============= STARTUP =============
if __name__ == "__main__":
    import os
    
    ensure_db_exists()
    print("\n" + "="*60)
    print("✓ GUARDIAN Backend v1.0 Initialized")
    print("="*60)
    print(f"✓ Database: {DB_FILE}")
    print("="*60 + "\n")
    
    # Start telemetry stream
    stream_thread = simulator.start_background_stream()
    
    # Get port from environment (for Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

    # Start telemetry stream
    stream_thread = simulator.start_background_stream()

    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)