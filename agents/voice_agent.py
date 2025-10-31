import json
from datetime import datetime
import random

class AIVoiceAgent:
    """AI-powered voice agent for customer engagement via WhatsApp"""

    def __init__(self):
        self.name = "AIVoiceAgent"
        self.conversation_history = []

    def generate_persuasive_message(self, vehicle_data, failure_prediction):
        """Generate contextual, persuasive message based on risk level"""

        risk_level = failure_prediction.get('risk_level')
        failure_prob = failure_prediction.get('failure_probability', 0)
        component = failure_prediction.get('predicted_failures', [{}])[0].get('component', 'component')

        if risk_level == "CRITICAL":
            message = f"""🚨 *URGENT: {vehicle_data['vehicle_id']} Needs Immediate Attention*

Dear {vehicle_data['owner_name']},

Our AI detected a *CRITICAL* issue with your {vehicle_data['model']}:

⚠️ *{component.title()} Failure Risk: {failure_prob}%*
📅 *Estimated Failure: Within 3 days*

*What This Means:*
• Your vehicle could break down unexpectedly
• Repair cost if ignored: ₹75,000+ (towing + emergency)
• Preventive maintenance now: ₹28,000

💡 *Recommendation:*
Schedule maintenance TODAY to avoid breakdown.

📞 Reply with preferred date/time!
- GUARDIAN AI Team"""

        elif risk_level == "HIGH":
            message = f"""⚠️ *Important: {vehicle_data['vehicle_id']} Maintenance*

Hi {vehicle_data['owner_name']},

Predictive check on your {vehicle_data['model']}:

🔧 *{component.title()} Issue Detected*
📊 *Failure Probability: {failure_prob}%*
📅 *Recommended Service: Within 7 days*

*Benefits of Early Action:*
✓ Save ₹40,000 in potential repair
✓ Prevent unexpected breakdowns
✓ Maintain warranty

Reply to schedule!
- GUARDIAN AI Team"""

        else:
            message = f"""ℹ️ *{vehicle_data['vehicle_id']} Routine Check*

Hello {vehicle_data['owner_name']},

Your {vehicle_data['model']} is due for routine maintenance.

📊 *Health Score: Good*
🛠️ *Recommended: Service within 30 days*

Schedule now for optimal performance!
- GUARDIAN AI Team"""

        return message

    def simulate_whatsapp_conversation(self, vehicle_data, prediction):
        """Simulate WhatsApp conversation flow"""

        conversation = {
            "vehicle_id": vehicle_data['vehicle_id'],
            "customer_name": vehicle_data['owner_name'],
            "phone": vehicle_data.get('phone_number', 'N/A'),
            "timestamp": datetime.now().isoformat(),
            "messages": [],
            "appointment_status": "PENDING"
        }

        # Initial AI message
        ai_message = self.generate_persuasive_message(vehicle_data, prediction)
        conversation['messages'].append({
            "from": "GUARDIAN AI",
            "message": ai_message,
            "time": "Now"
        })

        # Simulate customer response based on risk
        risk_level = prediction.get('risk_level')
        if risk_level == "CRITICAL":
            customer_response = "Yes, I want to schedule ASAP. Tomorrow morning?"
            acceptance_rate = 0.92
        elif risk_level == "HIGH":
            customer_response = "This week works. What slots available?"
            acceptance_rate = 0.78
        else:
            customer_response = "Will schedule next month"
            acceptance_rate = 0.45

        conversation['messages'].append({
            "from": vehicle_data['owner_name'],
            "message": customer_response,
            "time": "2 min ago"
        })

        # AI follow-up
        if random.random() < acceptance_rate:
            ai_response = f"""✅ *Appointment Confirmed!*

📍 Service Center: SC_1 (Delhi)
📅 Date: Tomorrow, 10:00 AM
👨‍🔧 Technician: Raj Kumar

*What to Expect:*
• Inspection: 30 min
• Repair: ~2 hours
• Cost: ₹28,000

Reminder 2 hours before. See you! 🚗"""
            conversation['appointment_status'] = "CONFIRMED"
        else:
            ai_response = "No problem! Reminder next week. Stay safe! 🚗"
            conversation['appointment_status'] = "DECLINED"

        conversation['messages'].append({
            "from": "GUARDIAN AI",
            "message": ai_response,
            "time": "1 min ago"
        })

        # Metrics
        conversation['metrics'] = {
            "acceptance_rate": int(acceptance_rate * 100),
            "response_time": "2 minutes",
            "customer_satisfaction": random.randint(85, 98),
            "cost_saved": 47000 if conversation['appointment_status'] == 'CONFIRMED' else 0
        }

        return conversation

if __name__ == "__main__":
    agent = AIVoiceAgent()

    vehicle = {
        "vehicle_id": "VH1001",
        "owner_name": "Rajesh Kumar",
        "model": "Hero Splendor",
        "phone_number": "9812345678"
    }

    prediction = {
        "risk_level": "CRITICAL",
        "failure_probability": 89,
        "predicted_failures": [{"component": "bearing", "failure_probability": 89}]
    }

    conversation = agent.simulate_whatsapp_conversation(vehicle, prediction)
    print(json.dumps(conversation, indent=2))