from datetime import datetime
from data_analysis_agent import DataAnalysisAgent
from diagnosis_agent import DiagnosisAgent
from engagement_agent import CustomerEngagementAgent
from scheduling_agent import SchedulingAgent
from quality_agent import ManufacturingQualityAgent
from ueba_agent import UEBAMonitor

class MasterAgent:
    def __init__(self):
        self.name = "MasterAgent"
        self.data_analysis = DataAnalysisAgent()
        self.diagnosis = DiagnosisAgent()
        self.engagement = CustomerEngagementAgent()
        self.scheduling = SchedulingAgent()
        self.quality = ManufacturingQualityAgent()
        self.ueba = UEBAMonitor()
        print(f"\n✓ {self.name} initialized with all worker agents\n")
    
    def orchestrate_workflow(self, vehicle_id):
        print(f"\n{'='*60}")
        print(f"🚀 WORKFLOW: {vehicle_id}")
        print(f"{'='*60}\n")
        
        workflow_results = {
            "workflow_id": f"WF_{datetime.now().timestamp()}",
            "vehicle_id": vehicle_id,
            "steps": [],
        }
        
        print("📊 STEP 1: Health Analysis...")
        health_report = self.data_analysis.generate_health_report(vehicle_id)
        workflow_results['steps'].append(("Health Analysis", health_report))
        print(f"   ✓ Health Score: {health_report['health_score']}/100")
        print(f"   ✓ Risk Level: {health_report['risk_level']}\n")
        
        if health_report['risk_level'] != 'LOW':
            print("🔧 STEP 2: Diagnosis...")
            diagnosis = self.diagnosis.predict_failures(vehicle_id)
            workflow_results['steps'].append(("Diagnosis", diagnosis))
            print(f"   ✓ Failure Probability: {diagnosis['failure_probability']}%\n")
            
            if diagnosis['predicted_failures']:
                print("📞 STEP 3: Customer Engagement...")
                engagement = self.engagement.initiate_outreach(vehicle_id, diagnosis)
                workflow_results['steps'].append(("Engagement", engagement))
                
                if engagement.get('customer_agreed'):
                    print(f"   ✓ Customer Agreed: YES\n")
                    
                    print("📅 STEP 4: Scheduling...")
                    appointment = self.scheduling.schedule_appointment(vehicle_id)
                    workflow_results['steps'].append(("Appointment", appointment))
                    print(f"   ✓ Booked: {appointment['date']} {appointment['time']}\n")
        
        print("🏭 STEP 5: Manufacturing Insights...")
        quality_insights = self.quality.analyze_failure_patterns(vehicle_id)
        workflow_results['steps'].append(("Quality", quality_insights))
        print(f"   ✓ CAPA Matches: {len(quality_insights['capa_matches'])}\n")
        
        print("🔒 STEP 6: Security Check...")
        security_report = self.ueba.generate_security_report()
        workflow_results['steps'].append(("Security", security_report))
        print(f"   ✓ Status: {security_report['security_status']}\n")
        
        print(f"{'='*60}")
        print(f"✅ WORKFLOW COMPLETE")
        print(f"{'='*60}\n")
        
        return workflow_results

if __name__ == "__main__":
    master = MasterAgent()
    for vehicle_id in ["VH1001", "VH1002"]:
        master.orchestrate_workflow(vehicle_id)
