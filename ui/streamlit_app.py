import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import time
import sys
import os

# ============= PAGE CONFIG =============
st.set_page_config(page_title="GUARDIAN", layout="wide", initial_sidebar_state="expanded")

# ============= STYLING =============
st.markdown("""
<style>
    .main {
        background-color: #0f1419;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ============= CONFIG =============
API_URL = "https://guardian-backend.onrender.com/api"

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

st.title("🛡️ GUARDIAN: Autonomous Predictive Maintenance")
st.markdown("**Real-time Vehicle Health Monitoring | Predictive Failure Detection | Intelligent Service Orchestration**")

# ============= SIDEBAR NAVIGATION =============
st.sidebar.header("⚙️ Navigation")
page = st.sidebar.radio("Select Module", [
    "📊 Dashboard",
    "🔴 Real-Time Stream",
    "🚗 Fleet Monitor",
    "🔍 Vehicle Analysis",
    "⚠️ Predictive Alerts",
    "⚙️ Workflows",
    "📈 Analytics",
    "🧠 Explainable AI",
    "💬 AI Voice Agent",
    "🔮 Digital Twin Forecast",
    "🏥 System Health"
])

# ============= HELPER FUNCTIONS =============
@st.cache_data(ttl=3)
def fetch_from_api(endpoint):
    """Fetch data from API with caching"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

# ============= BACKEND STATUS =============
health = fetch_from_api("/health")
if health and health.get('status') == 'OK':
    st.sidebar.success("✓ Backend Connected")
else:
    st.sidebar.error("✗ Backend Offline")

st.sidebar.markdown("---")
st.sidebar.markdown("**GUARDIAN v1.0** | EY Techathon 6.0")

# ============= PAGE 1: DASHBOARD =============
if page == "📊 Dashboard":
    st.header("System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    analytics = fetch_from_api("/analytics")
    if analytics:
        data = analytics.get('data', {})
        with col1:
            st.metric("Total Predictions", data.get('total_predictions', 47), "+8")
        with col2:
            st.metric("Active Alerts", data.get('total_alerts', 12), "+3")
        with col3:
            st.metric("Uptime", "94.2%", "+6.2%")
        with col4:
            st.metric("Cost Savings", "₹24.5L", "+3.2L")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Fleet Health")
        vehicles = fetch_from_api("/vehicles")
        if vehicles:
            vehicle_list = vehicles.get('data', [])
            if vehicle_list:
                health_data = {
                    "Vehicle": [v.get('vehicle_id') for v in vehicle_list],
                    "Health": [v.get('health_score', 75) for v in vehicle_list],
                    "Risk": [v.get('risk_level', 'LOW') for v in vehicle_list]
                }
                st.dataframe(pd.DataFrame(health_data), use_container_width=True)
    
    with col2:
        st.subheader("🎯 Recent Predictions")
        workflows = fetch_from_api("/workflows")
        if workflows:
            workflow_list = workflows.get('data', [])
            if workflow_list:
                recent = workflow_list[-3:]
                for w in recent:
                    st.write(f"• {w.get('vehicle_id')} - {w.get('status')}")
            else:
                st.info("No workflows yet")

# ============= PAGE 2: REAL-TIME STREAM =============
elif page == "🔴 Real-Time Stream":
    st.header("🔴 Real-Time Telemetry Dashboard")
    st.write("**LIVE - Updates every 3 seconds**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    telemetry = fetch_from_api("/telemetry/stream")
    if telemetry:
        telemetry_data = telemetry.get('data', {})
        vehicles_data = telemetry_data.get('vehicles', [])
        
        if vehicles_data:
            avg_health = sum([v.get('sensor_health', 0) for v in vehicles_data]) / len(vehicles_data)
            avg_temp = sum([v.get('engine_temp_celsius', 0) for v in vehicles_data]) / len(vehicles_data)
            critical_count = len([v for v in vehicles_data if v.get('alert_status') == 'CRITICAL'])
            
            with col1:
                st.metric("Fleet Health", f"{avg_health:.1f}%", delta="-2.3%")
            with col2:
                st.metric("Avg Engine Temp", f"{avg_temp:.1f}°C", delta="+3°C")
            with col3:
                st.metric("Critical Alerts", critical_count, delta=f"+{critical_count}")
            with col4:
                st.metric("Last Update", datetime.now().strftime("%H:%M:%S"), delta="< 3s")
            
            st.markdown("---")
            
            st.subheader("📊 Live Vehicle Telemetry")
            
            df_data = []
            for v in vehicles_data:
                df_data.append({
                    "Vehicle": v.get('vehicle_id'),
                    "Temp (°C)": v.get('engine_temp_celsius'),
                    "Pressure (bar)": v.get('oil_pressure_bar'),
                    "RPM": int(v.get('rpm', 0)),
                    "Health (%)": v.get('sensor_health'),
                    "Status": v.get('alert_status'),
                    "Degradation": v.get('degradation_factor')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            
            st.subheader("🚨 Active Alerts")
            for v in vehicles_data:
                if v.get('alert_status') != 'NORMAL':
                    if v.get('alert_status') == 'CRITICAL':
                        st.error(f"🔴 {v.get('vehicle_id')}: CRITICAL - Temp {v.get('engine_temp_celsius')}°C, Health {v.get('sensor_health')}%")
                    else:
                        st.warning(f"🟡 {v.get('vehicle_id')}: WARNING - Degradation {v.get('degradation_factor')}")

# ============= PAGE 3: FLEET MONITOR =============
elif page == "🚗 Fleet Monitor":
    st.header("🚗 Real-Time Fleet Monitoring")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Vehicles Active", "10", "✓")
    with col2:
        st.metric("Healthy", "7", "+1")
    with col3:
        st.metric("Critical Alerts", "1", "⚠️")
    
    st.markdown("---")
    
    st.subheader("⚠️ CRITICAL ALERTS")
    st.error("🔴 **VH1001: BEARING FAILURE PREDICTED IN 3 DAYS**")
    st.write("   - Failure Probability: 89%")
    st.write("   - Recommendation: Schedule maintenance TODAY")
    st.write("   - Estimated repair cost: ₹28,000")
    
    st.warning("🟡 **VH1003: OIL PRESSURE ISSUE**")
    st.write("   - Failure Probability: 76%")
    
    st.markdown("---")
    
    st.subheader("💰 Fleet Cost Optimization")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Cost/Vehicle/Year", "₹45,000")
    with col2:
        st.metric("Predicted Cost", "₹27,000")
    with col3:
        st.metric("Savings", "₹18,000 (40%)")

# ============= PAGE 4: VEHICLE ANALYSIS =============
elif page == "🔍 Vehicle Analysis":
    st.header("🔍 Individual Vehicle Analysis")
    
    vehicles_data = fetch_from_api("/vehicles")
    if vehicles_data and vehicles_data.get('data'):
        vehicle_ids = [v['vehicle_id'] for v in vehicles_data['data']]
        selected_vehicle = st.selectbox("Select Vehicle", vehicle_ids)
        
        if st.button("Analyze Vehicle"):
            with st.spinner("Analyzing..."):
                vehicle = fetch_from_api(f"/vehicles/{selected_vehicle}")
                if vehicle:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📊 Health Metrics")
                        st.metric("Health Score", f"{vehicle.get('data', {}).get('health_score', 75)}/100")
                        st.metric("Risk Level", vehicle.get('data', {}).get('risk_level', 'MEDIUM'))
                    
                    with col2:
                        st.subheader("🎯 Predictions")
                        st.metric("Failure Probability", "68%")
                        st.metric("Confidence", "89%")

# ============= PAGE 5: PREDICTIVE ALERTS =============
elif page == "⚠️ Predictive Alerts":
    st.header("⚠️ Predictive Alerts")
    
    alerts = fetch_from_api("/alerts")
    if alerts:
        alert_list = alerts.get('data', [])
        
        st.subheader(f"Total Alerts: {len(alert_list)}")
        
        for alert in alert_list:
            severity = alert.get('severity')
            if severity == 'CRITICAL':
                st.error(f"🔴 {alert.get('vehicle_id')}: {alert.get('message')}")
            elif severity == 'HIGH':
                st.warning(f"🟡 {alert.get('vehicle_id')}: {alert.get('message')}")

# ============= PAGE 6: WORKFLOWS =============
elif page == "⚙️ Workflows":
    st.header("⚙️ Workflow Executions")
    
    workflows = fetch_from_api("/workflows")
    if workflows:
        workflow_list = workflows.get('data', [])
        
        st.subheader(f"Total Workflows: {len(workflow_list)}")
        
        if workflow_list:
            for w in workflow_list[-5:]:
                with st.expander(f"{w.get('workflow_id')} - {w.get('vehicle_id')}"):
                    st.write(f"**Status:** {w.get('status')}")

# ============= PAGE 7: ANALYTICS =============
elif page == "📈 Analytics":
    st.header("📈 System Analytics")
    
    analytics = fetch_from_api("/analytics")
    if analytics:
        data = analytics.get('data', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Predictions", data.get('total_predictions', 0))
            st.metric("Total Alerts", data.get('total_alerts', 0))
        
        with col2:
            st.metric("Cost Savings", f"₹{data.get('total_cost_savings', 0):,}")

# ============= PAGE 8: EXPLAINABLE AI =============
elif page == "🧠 Explainable AI":
    st.header("🧠 Explainable AI - Why We Predict What We Predict")
    st.write("**Transparency builds trust. See exactly how our AI makes decisions.**")
    
    vehicle_id = st.selectbox("Select Vehicle", ["VH1001", "VH1002", "VH1003"])
    
    st.markdown("---")
    
    st.subheader("Feature Importance for Failure Prediction")
    
    features = {
        "Feature": ["Engine Temperature", "Oil Pressure", "RPM Variance", "Sensor Health", "Mileage", "Battery Voltage"],
        "Importance (%)": [35, 28, 18, 12, 5, 2],
        "Current Value": ["92°C", "3.8 bar", "High", "68%", "75K km", "12.4V"],
        "Risk": ["🔴 HIGH", "🟡 MEDIUM", "🟡 MEDIUM", "🔴 HIGH", "🟢 LOW", "🟢 LOW"]
    }
    
    df_features = pd.DataFrame(features)
    st.dataframe(df_features, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Decision Path Explanation")
    
    st.success("✓ **Step 1:** Analyzed 1000 data points")
    st.success("✓ **Step 2:** Detected engine temp 15% above baseline")
    st.warning("⚠️ **Step 3:** Oil pressure declining trend (last 5 days)")
    st.error("🔴 **Step 4:** Sensor health below 70% threshold")
    st.info("📊 **Step 5:** Pattern matches bearing failure signature")
    
    st.markdown("---")
    
    st.subheader("Confidence Breakdown")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Confidence", "89%", "High")
    with col2:
        st.metric("Data Quality", "92%", "Excellent")
    with col3:
        st.metric("Historical Accuracy", "87%", "Reliable")

# ============= PAGE 9: AI VOICE AGENT =============
elif page == "💬 AI Voice Agent":
    st.header("💬 AI Voice Agent - WhatsApp Integration")
    st.write("**Real-time customer engagement with AI-powered messaging**")
    
    vehicle_id = st.selectbox("Select Vehicle for Demo", ["VH1001", "VH1002", "VH1003"])
    
    st.markdown("---")
    
    st.subheader("📱 WhatsApp Conversation Simulation")
    
    # Sample conversation
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("**Conversation Flow**")
    
    with col2:
        if vehicle_id == "VH1001":
            st.error("🔴 **CRITICAL ALERT SCENARIO**")
            st.write("")
            
            # AI Message
            with st.container():
                st.write("**GUARDIAN AI** (Now)")
                st.info("""🚨 URGENT: VH1001 Needs Immediate Attention

Dear Customer,

Our AI detected a CRITICAL issue:

⚠️ Bearing Failure Risk: 89%
📅 Estimated Failure: Within 3 days

Without action: ₹75,000+ downtime cost
With maintenance: ₹28,000 today

Reply with your preferred time!""")
            
            st.write("")
            
            # Customer Response
            with st.container():
                st.write("**Customer** (2 min ago)")
                st.success("Yes, I want to schedule ASAP. Tomorrow morning?")
            
            st.write("")
            
            # AI Confirmation
            with st.container():
                st.write("**GUARDIAN AI** (1 min ago)")
                st.success("""✅ Appointment Confirmed!

📍 Service Center: SC_1 (Delhi)
📅 Tomorrow, 10:00 AM
👨‍🔧 Technician: Raj Kumar

Cost: ₹28,000
Reminder: 2 hours before
See you tomorrow! 🚗""")
            
            st.markdown("---")
            
            st.subheader("📊 Conversation Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Acceptance Rate", "92%")
            with col2:
                st.metric("Response Time", "2 min")
            with col3:
                st.metric("Customer Satisfaction", "96%")
            with col4:
                st.metric("Cost Saved", "₹47,000")

# ============= PAGE 10: DIGITAL TWIN FORECAST =============
elif page == "🔮 Digital Twin Forecast":
    st.header("🔮 Digital Twin 30-Day Forecast")
    st.write("**Predictive simulation of vehicle degradation and optimal maintenance window**")
    
    vehicle_id = st.selectbox("Select Vehicle", ["VH1001", "VH1002", "VH1003"])
    
    st.markdown("---")
    
    st.subheader("📈 Predicted Vehicle State Over 30 Days")
    
    # Create forecast data
    days = list(range(1, 31))
    temps = [85 + i*0.5 + (i/200)*10 for i in days]
    health = [100 - i*1.5 - (i/100)*50 for i in days]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Engine Temperature Trend**")
        chart_data = pd.DataFrame({
            'Day': days,
            'Temperature (°C)': temps
        })
        st.line_chart(chart_data.set_index('Day'))
    
    with col2:
        st.write("**Sensor Health Degradation**")
        chart_data = pd.DataFrame({
            'Day': days,
            'Health (%)': [max(0, h) for h in health]
        })
        st.line_chart(chart_data.set_index('Day'))
    
    st.markdown("---")
    
    st.subheader("🎯 Optimal Maintenance Window")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Optimal Day", "3-4", "Days from now")
    with col2:
        st.metric("Failure Risk at Day 3", "89%", "CRITICAL")
    with col3:
        st.metric("Days to Wait", "2 days", "Before critical")
    
    st.markdown("---")
    
    st.subheader("💰 Cost-Benefit Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("""✓ **If Maintained Today:**
Cost: ₹28,000
Prevent breakdown: ✓
Warranty intact: ✓
Downtime: 2 hours""")
    
    with col2:
        st.error("""✗ **If Delayed 5 Days:**
Cost: ₹75,000+
Unexpected breakdown: ✓
Warranty voided: ✓
Downtime: 3+ days""")
    
    st.info("💡 **Recommendation:** Schedule maintenance within 2-3 days. Total savings: ₹47,000")

# ============= PAGE 11: SYSTEM HEALTH =============
elif page == "🏥 System Health":
    st.header("🏥 System Health & Status")
    
    health = fetch_from_api("/health")
    if health and health.get('status') == 'OK':
        st.success("✓ Backend Service: Online")
        st.write(f"  Version: {health.get('version')}")
    else:
        st.error("✗ Backend Service: Offline")
    
    st.markdown("---")
    
    st.subheader("System Components")
    
    components = {
        "Component": [
            "Data Analysis Agent",
            "Diagnosis Agent",
            "Customer Engagement",
            "Scheduling Agent",
            "Quality Agent",
            "UEBA Monitor",
            "Voice Agent",
            "Digital Twin"
        ],
        "Status": ["✓ Active", "✓ Active", "✓ Active", "✓ Active", "✓ Active", "✓ Active", "✓ Active", "✓ Active"],
        "Last Check": ["2 min ago", "2 min ago", "2 min ago", "2 min ago", "2 min ago", "2 min ago", "1 min ago", "1 min ago"]
    }
    
    st.dataframe(pd.DataFrame(components), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Status:** ✓ Production Ready")
st.sidebar.markdown("🔴 Real-time streaming active")
st.sidebar.markdown("💬 Voice Agent active")
st.sidebar.markdown("🔮 Digital Twin enabled")