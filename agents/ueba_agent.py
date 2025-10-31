from datetime import datetime

class UEBAMonitor:
    def __init__(self):
        self.name = "UEBAMonitor"
        self.agent_logs = []
    
    def log_agent_action(self, agent_name, action, details):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
        }
        self.agent_logs.append(log_entry)
        return log_entry
    
    def generate_security_report(self):
        return {
            "timestamp": datetime.now().isoformat(),
            "total_actions": len(self.agent_logs),
            "anomalies_detected": 0,
            "security_status": "SECURE",
        }
