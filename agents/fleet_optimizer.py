import json
from datetime import datetime, timedelta

class FleetOptimizer:
    """Optimize fleet-wide maintenance scheduling"""

    def __init__(self):
        self.name = "FleetOptimizer"

    def optimize_maintenance_schedule(self, vehicles):
        """Optimize when and where to schedule maintenance"""

        schedule = []

        for vehicle in vehicles:
            risk = vehicle.get('risk_level', 'LOW')

            # Priority scoring
            if risk == 'CRITICAL':
                priority = 1
                urgency = "Immediate"
                max_delay_days = 2
            elif risk == 'HIGH':
                priority = 2
                urgency = "This Week"
                max_delay_days = 7
            elif risk == 'MEDIUM':
                priority = 3
                urgency = "This Month"
                max_delay_days = 30
            else:
                priority = 4
                urgency = "Next Quarter"
                max_delay_days = 90

            schedule.append({
                "vehicle_id": vehicle['vehicle_id'],
                "priority": priority,
                "urgency": urgency,
                "max_delay_days": max_delay_days,
                "assigned_center": "SC_1",
                "estimated_slot": (datetime.now() + timedelta(days=priority)).strftime("%Y-%m-%d"),
                "estimated_cost": self._estimate_cost(risk),
                "downtime_hours": 3 if risk == 'CRITICAL' else 2
            })

        # Sort by priority
        schedule.sort(key=lambda x: x['priority'])

        return schedule

    def _estimate_cost(self, risk):
        """Estimate maintenance cost based on risk"""
        costs = {
            'CRITICAL': 28000,
            'HIGH': 22000,
            'MEDIUM': 15000,
            'LOW': 8000
        }
        return costs.get(risk, 10000)

    def calculate_fleet_roi(self, schedule):
        """Calculate ROI for entire fleet"""

        total_proactive_cost = sum([s['estimated_cost'] for s in schedule])

        # Without GUARDIAN - assume 40% fail unexpectedly
        reactive_cost = total_proactive_cost * 1.6 + (len(schedule) * 0.4 * 75000)

        savings = reactive_cost - total_proactive_cost
        roi_percentage = (savings / total_proactive_cost) * 100 if total_proactive_cost > 0 else 0

        return {
            "total_fleet_size": len(schedule),
            "proactive_maintenance_cost": total_proactive_cost,
            "reactive_cost_without_guardian": reactive_cost,
            "total_savings": savings,
            "roi_percentage": round(roi_percentage, 1),
            "payback_period_months": 4,
            "vehicles_critical": len([s for s in schedule if s['priority'] == 1]),
            "vehicles_high_risk": len([s for s in schedule if s['priority'] == 2])
        }

if __name__ == "__main__":
    optimizer = FleetOptimizer()

    vehicles = [
        {"vehicle_id": "VH1001", "risk_level": "CRITICAL"},
        {"vehicle_id": "VH1002", "risk_level": "LOW"},
        {"vehicle_id": "VH1003", "risk_level": "HIGH"}
    ]

    schedule = optimizer.optimize_maintenance_schedule(vehicles)
    roi = optimizer.calculate_fleet_roi(schedule)

    print(f"Total Savings: ₹{roi['total_savings']:,}")
    print(f"ROI: {roi['roi_percentage']}%")