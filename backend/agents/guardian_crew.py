import os
import json
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from datetime import datetime, timedelta

# ============= TOOLS (What agents can use) =============

class AnalyzeVehicleDataTool(BaseTool):
    name: str = "Analyze Vehicle Data"
    description: str = "Analyzes raw sensor data and detects anomalies"
    
    def _run(self, vehicle_id: str, sensor_data: dict) -> str:
        health_score = sensor_data.get('sensor_health', 75)
        temp = sensor_data.get('engine_temp_celsius', 85)
        pressure = sensor_data.get('oil_pressure_bar', 3.5)
        
        issues = []
        if temp > 100:
            issues.append(f"High engine temperature: {temp}°C")
        if pressure < 2.5:
            issues.append(f"Low oil pressure: {pressure} bar")
        if health_score < 70:
            issues.append(f"Sensor health degraded: {health_score}%")
        
        return f"Vehicle {vehicle_id} Analysis: {', '.join(issues) if issues else 'All systems normal'}"

class PredictFailureTool(BaseTool):
    name: str = "Predict Failure"
    description: str = "Predicts potential failures based on analysis"
    
    def _run(self, vehicle_id: str, analysis: str) -> str:
        if "High engine temperature" in analysis:
            return f"Vehicle {vehicle_id}: Bearing failure risk 89%, Days to failure: 3-5"
        elif "Low oil pressure" in analysis:
            return f"Vehicle {vehicle_id}: Oil system failure risk 76%, Days to failure: 7-10"
        else:
            return f"Vehicle {vehicle_id}: All systems healthy, no critical risks detected"

class DraftCustomerMessageTool(BaseTool):
    name: str = "Draft Customer Message"
    description: str = "Drafts personalized customer engagement message"
    
    def _run(self, vehicle_id: str, prediction: str) -> str:
        if "89%" in prediction:
            msg = f"🚨 URGENT: Your vehicle {vehicle_id} needs immediate attention. Bearing failure predicted in 3-5 days. Click to schedule service TODAY."
        elif "76%" in prediction:
            msg = f"⚠️ WARNING: Your vehicle {vehicle_id} showing signs of oil system issues. Schedule maintenance within a week to avoid breakdowns."
        else:
            msg = f"✓ Your vehicle {vehicle_id} is running smoothly. Regular checkup recommended in 2 months."
        
        return msg

class ScheduleServiceTool(BaseTool):
    name: str = "Schedule Service"
    description: str = "Schedules service appointment"
    
    def _run(self, vehicle_id: str, urgency: str) -> str:
        service_centers = ["SC_Delhi_1", "SC_Delhi_2", "SC_Bangalore_1"]
        center = service_centers[hash(vehicle_id) % len(service_centers)]
        
        if "URGENT" in urgency:
            return f"Service scheduled for {vehicle_id} at {center} - TOMORROW 9:00 AM (slots: 2 available)"
        else:
            return f"Service can be scheduled for {vehicle_id} at {center} - Next week available"

class CalculateROITool(BaseTool):
    name: str = "Calculate ROI"
    description: str = "Calculates cost-benefit of preventive maintenance"
    
    def _run(self, vehicle_id: str, failure_type: str) -> str:
        if "Bearing" in failure_type:
            preventive_cost = 28000
            breakdown_cost = 75000
            savings = breakdown_cost - preventive_cost
            return f"ROI for {vehicle_id}: Maintain now (₹{preventive_cost}) vs. wait and break (₹{breakdown_cost}). Savings: ₹{savings}"
        else:
            preventive_cost = 15000
            breakdown_cost = 50000
            savings = breakdown_cost - preventive_cost
            return f"ROI for {vehicle_id}: Maintain now (₹{preventive_cost}) vs. wait and break (₹{breakdown_cost}). Savings: ₹{savings}"

# ============= AGENTS (Autonomous Workers) =============

def create_guardian_crew(vehicle_id: str, sensor_data: dict):
    """Creates and orchestrates the GUARDIAN agent crew."""
    
    # Initialize tools
    analyze_tool = AnalyzeVehicleDataTool()
    predict_tool = PredictFailureTool()
    message_tool = DraftCustomerMessageTool()
    schedule_tool = ScheduleServiceTool()
    roi_tool = CalculateROITool()
    
    # DIAGNOSIS AGENT
    diagnosis_agent = Agent(
        role="Diagnostic Specialist",
        goal="Analyze vehicle sensor data and predict potential failures accurately",
        backstory="Expert vehicle diagnostician with access to real-time sensor analytics and ML models",
        tools=[analyze_tool, predict_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # CUSTOMER ENGAGEMENT AGENT
    engagement_agent = Agent(
        role="Customer Engagement Specialist",
        goal="Craft personalized, persuasive messages that encourage preventive maintenance",
        backstory="Expert in customer communication with high conversion rates for service bookings",
        tools=[message_tool, schedule_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # ROI OPTIMIZATION AGENT
    roi_agent = Agent(
        role="Business Analyst",
        goal="Quantify cost savings and ROI for every maintenance decision",
        backstory="Financial analyst specializing in fleet cost optimization",
        tools=[roi_tool],
        verbose=True,
        allow_delegation=False
    )
    
    # MASTER ORCHESTRATOR AGENT
    master_agent = Agent(
        role="Fleet Operations Master",
        goal="Orchestrate diagnosis, engagement, and optimization to achieve vehicle health goals",
        backstory="Senior fleet operations manager who oversees all maintenance decisions",
        verbose=True,
        allow_delegation=True
    )
    
    # ============= TASKS =============
    
    task_diagnosis = Task(
        description=f"Analyze sensor data for vehicle {vehicle_id}: {json.dumps(sensor_data)}. Use the analysis and prediction tools to determine failure risks.",
        agent=diagnosis_agent,
        expected_output="Detailed analysis with failure prediction and risk percentage"
    )
    
    task_engagement = Task(
        description=f"Based on the diagnosis results, draft a personalized customer message for vehicle {vehicle_id} and determine if service should be scheduled immediately.",
        agent=engagement_agent,
        expected_output="Personalized customer message and service scheduling recommendation"
    )
    
    task_roi = Task(
        description=f"Calculate the ROI of preventive maintenance for vehicle {vehicle_id} based on the predicted failure type.",
        agent=roi_agent,
        expected_output="Clear cost-benefit analysis with savings amount"
    )
    
    task_master = Task(
        description=f"Review all agent outputs and deliver a final maintenance recommendation for {vehicle_id}.",
        agent=master_agent,
        expected_output="Final decision: maintenance urgency, customer action, and ROI summary"
    )
    
    # ============= CREW =============
    
    crew = Crew(
        agents=[diagnosis_agent, engagement_agent, roi_agent, master_agent],
        tasks=[task_diagnosis, task_engagement, task_roi, task_master],
        verbose=True
    )
    
    return crew

# ============= MAIN FUNCTION =============

def run_guardian_crew(vehicle_id: str, sensor_data: dict) -> dict:
    """Execute the GUARDIAN agentic crew."""
    try:
        crew = create_guardian_crew(vehicle_id, sensor_data)
        result = crew.kickoff()
        
        return {
            "vehicle_id": vehicle_id,
            "timestamp": datetime.now().isoformat(),
            "crew_output": str(result),
            "status": "Autonomous decision completed"
        }
    except Exception as e:
        return {
            "vehicle_id": vehicle_id,
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "status": "Error in crew execution"
        }
