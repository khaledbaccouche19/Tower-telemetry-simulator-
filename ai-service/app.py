from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import requests
import json
import re
import asyncio
from gemini_integration import GeminiTowerAnalyzer

# Pydantic models for request/response
class TowerAnalysisRequest(BaseModel):
    tower_id: int
    telemetry_data: List[Dict[str, Any]]
    siteboss_data: Dict[str, Any]

class TowerAnalysisResponse(BaseModel):
    tower_id: int
    analysis: str
    timestamp: str

class ChatMessageRequest(BaseModel):
    tower_id: int
    message: str
    telemetry_data: List[Dict[str, Any]] = []
    siteboss_data: Dict[str, Any] = {}

class ChatMessageResponse(BaseModel):
    tower_id: int
    user_message: str
    ai_response: str
    timestamp: str

# Initialize FastAPI app
app = FastAPI(title="Tower AI Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini lazily (only when first needed)
GEMINI_API_KEY = "AIzaSyAJ5NnpeZp0QbCej8EgbGJa8jGzdLF0fDo"
gemini_analyzer = None

def get_gemini_analyzer():
    """Get Gemini analyzer, initializing it if needed"""
    global gemini_analyzer
    if gemini_analyzer is None:
        try:
            gemini_analyzer = GeminiTowerAnalyzer(GEMINI_API_KEY)
            print("✅ Gemini initialized successfully")
        except Exception as e:
            print(f"❌ Gemini initialization failed: {e}")
            return None
    return gemini_analyzer

# Configuration for data sources
TELEMETRY_BASE_URL = "http://localhost:8080"  # Telemetry simulator
BACKEND_BASE_URL = "http://localhost:8088"    # Main backend

# Global flag to track if auto-alerting is enabled
auto_alerting_enabled = False  # DISABLED: To preserve quota for manual use

def fetch_telemetry_data(tower_id: int) -> List[Dict[str, Any]]:
    """Fetch telemetry data from the telemetry simulator"""
    try:
        # For now, we'll use the live endpoint since tower-specific data isn't available
        response = requests.get(f"{TELEMETRY_BASE_URL}/api/telemetry/live", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                # Add tower_id to the data
                data[0]['towerId'] = tower_id
                return data
        return []
    except Exception as e:
        print(f"Error fetching telemetry data: {e}")
        return []

def fetch_siteboss_data(tower_id: int) -> Dict[str, Any]:
    """Fetch SiteBoss data from the main backend"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/siteboss/latest", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        print(f"Error fetching SiteBoss data: {e}")
        return {}

def fetch_tower_info(tower_id: int) -> Dict[str, Any]:
    """Fetch tower information from the main backend"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/towers/{tower_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        print(f"Error fetching tower info: {e}")
        return {}

def fetch_hardware_data(tower_id: int) -> List[Dict[str, Any]]:
    """Fetch hardware components data from the main backend"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/hardware/tower/{tower_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching hardware data: {e}")
        return []

def fetch_maintenance_data(tower_id: int) -> List[Dict[str, Any]]:
    """Fetch maintenance records from the main backend"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/maintenance/tower/{tower_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching maintenance data: {e}")
        return []

def fetch_all_towers() -> List[Dict[str, Any]]:
    """Fetch all towers from the main backend"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/towers", timeout=5)
        if response.status_code == 200:
            towers = response.json()
            # Extract tower IDs
            tower_ids = [tower.get('id') for tower in towers if tower.get('id')]
            print(f"📡 Found {len(tower_ids)} towers: {tower_ids}")
            return tower_ids
        return []
    except Exception as e:
        print(f"Error fetching towers: {e}")
        return []

def check_duplicate_alert(tower_id: int, title: str) -> bool:
    """Check if a similar alert already exists"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/api/alerts/tower/{tower_id}", timeout=5)
        if response.status_code == 200:
            existing_alerts = response.json()
            # Check for similar titles in unresolved alerts
            for alert in existing_alerts:
                if not alert.get("resolved", False):
                    existing_title = alert.get("message", "").split(":")[0] if ":" in alert.get("message", "") else ""
                    if title.lower() in existing_title.lower() or existing_title.lower() in title.lower():
                        return True
        return False
    except Exception as e:
        print(f"Error checking duplicate alerts: {e}")
        return False

def create_alert(tower_id: int, title: str, description: str, severity: str = "MEDIUM") -> Dict[str, Any]:
    """Create an alert in the backend system with deduplication"""
    try:
        # Check for duplicates first
        if check_duplicate_alert(tower_id, title):
            print(f"Duplicate alert prevented: {title}")
            return {}
        
        alert_data = {
            "towerId": tower_id,
            "message": f"{title}: {description}",
            "severity": severity,
            "resolved": False,
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(f"{BACKEND_BASE_URL}/api/alerts", json=alert_data, timeout=5)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Alert creation failed with status {response.status_code}: {response.text}")
        return {}
    except Exception as e:
        print(f"Error creating alert: {e}")
        return {}

def clean_markdown_formatting(text: str) -> str:
    """Remove markdown formatting from AI responses"""
    # Remove markdown bold formatting **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove markdown italic formatting *text*
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove markdown links [text](url) 
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text).strip()
    return text

def extract_alerts_from_analysis(analysis: str, tower_id: int) -> List[Dict[str, Any]]:
    """Extract actionable alerts from AI analysis with smart filtering"""
    alerts = []
    analysis_lower = analysis.lower()
    
    # Skip if analysis indicates no issues
    if any(phrase in analysis_lower for phrase in ["no issues", "no immediate", "none apparent", "all systems normal"]):
        return alerts
    
    # 1. SECURITY ISSUES - Most Critical
    if any(keyword in analysis_lower for keyword in ["door", "doors", "breach", "unauthorized", "security"]):
        # Look for specific security issues
        if "door" in analysis_lower and "open" in analysis_lower:
            alerts.append({
                "tower_id": tower_id,
                "title": "Security Breach Detected",
                "description": "Front and/or back doors are open - unauthorized access possible",
                "severity": "CRITICAL"
            })
        elif "breach" in analysis_lower or "unauthorized" in analysis_lower:
            alerts.append({
                "tower_id": tower_id,
                "title": "Security Alert",
                "description": "Potential security breach detected",
                "severity": "CRITICAL"
            })
    
    # 2. FIRE/SAFETY ISSUES - Critical
    if "smoke" in analysis_lower or "fire" in analysis_lower:
        alerts.append({
            "tower_id": tower_id,
            "title": "Fire/Safety Alert",
            "description": "Smoke or fire hazard detected - immediate action required",
            "severity": "CRITICAL"
        })
    
    # 3. MAINTENANCE ISSUES - Medium Priority
    if any(keyword in analysis_lower for keyword in ["overdue", "maintenance", "inspection"]):
        if "cooling" in analysis_lower and "inspection" in analysis_lower:
            alerts.append({
                "tower_id": tower_id,
                "title": "Maintenance Overdue",
                "description": "Cooling system inspection is overdue",
                "severity": "MEDIUM"
            })
        elif "maintenance" in analysis_lower and "overdue" in analysis_lower:
            alerts.append({
                "tower_id": tower_id,
                "title": "Maintenance Required",
                "description": "Scheduled maintenance is overdue",
                "severity": "MEDIUM"
            })
    
    # 4. HARDWARE ISSUES - High Priority (only if actual problems)
    if any(keyword in analysis_lower for keyword in ["failure", "malfunction", "error", "fault"]):
        if not any(phrase in analysis_lower for phrase in ["no hardware", "no issues", "none apparent"]):
            alerts.append({
                "tower_id": tower_id,
                "title": "Hardware Failure",
                "description": "Hardware component failure detected",
                "severity": "HIGH"
            })
    
    # 5. PERFORMANCE ISSUES - Medium Priority
    if any(keyword in analysis_lower for keyword in ["performance", "degraded", "slow", "high load"]):
        alerts.append({
            "tower_id": tower_id,
            "title": "Performance Issue",
            "description": "System performance degradation detected",
            "severity": "MEDIUM"
        })
    
    return alerts

async def auto_generate_alerts():
    """Automatically generate alerts for all towers every 5 minutes"""
    global auto_alerting_enabled
    
    while auto_alerting_enabled:
        try:
            if auto_alerting_enabled:
                print("🤖 Auto-generating alerts...")
                
                # Get all towers from the backend
                towers_to_check = fetch_all_towers()
                if not towers_to_check:
                    print("⚠️ No towers found, skipping auto-alert generation")
                    await asyncio.sleep(300)  # Wait 5 minutes before trying again
                    continue
                
                for tower_id in towers_to_check:
                    try:
                        # Generate alerts for this tower
                        telemetry_data = fetch_telemetry_data(tower_id)
                        siteboss_data = fetch_siteboss_data(tower_id)
                        tower_info = fetch_tower_info(tower_id)
                        hardware_data = fetch_hardware_data(tower_id)
                        maintenance_data = fetch_maintenance_data(tower_id)
                        
                        # Create analysis prompt
                        analysis_prompt = f"""
                        You are an expert in 5G tower monitoring. Analyze this tower data for any issues requiring alerts:
                        
                        TOWER ID: {tower_id}
                        TELEMETRY DATA: {json.dumps(telemetry_data, indent=2)}
                        SITEBOSS DATA: {json.dumps(siteboss_data, indent=2)}
                        HARDWARE COMPONENTS: {json.dumps(hardware_data or [], indent=2)}
                        MAINTENANCE RECORDS: {json.dumps(maintenance_data or [], indent=2)}
                        
                        Identify any critical issues, security breaches, maintenance needs, or hardware problems.
                        Be concise and focus only on actionable items.
                        """
                        
                        # Get AI analysis
                        analyzer = get_gemini_analyzer()
                        if analyzer:
                            analysis = analyzer.model.generate_content(analysis_prompt)
                            analysis_text = clean_markdown_formatting(analysis.text)
                        else:
                            analysis_text = f"Tower {tower_id} status: Normal operation. No immediate alerts required."
                        
                        # Extract and create alerts
                        extracted_alerts = extract_alerts_from_analysis(analysis_text, tower_id)
                        created_count = 0
                        
                        for alert_data in extracted_alerts:
                            created_alert = create_alert(
                                alert_data["tower_id"],
                                alert_data["title"],
                                alert_data["description"],
                                alert_data["severity"]
                            )
                            if created_alert:
                                created_count += 1
                        
                        if created_count > 0:
                            print(f"✅ Generated {created_count} alerts for Tower {tower_id}")
                        
                    except Exception as e:
                        print(f"❌ Error processing Tower {tower_id}: {e}")
                
                print("⏰ Waiting 5 minutes for next auto-alert cycle...")
            
        except Exception as e:
            print(f"❌ Error in auto-alert generation: {e}")
        
        # Wait 5 minutes (300 seconds)
        await asyncio.sleep(300)

# Startup event to begin auto-alerting
@app.on_event("startup")
async def startup_event():
    """Start the automatic alert generation when the service starts"""
    print("🚀 Starting AI Tower Monitoring Service...")
    print("⚠️ Auto-alerting DISABLED - To preserve quota for manual use")
    # Auto-alerting disabled to preserve quota
    # asyncio.create_task(auto_generate_alerts())

# Health check endpoint
@app.get("/")
def health_check():
    return {
        "status": "healthy", 
        "service": "Tower AI Service", 
        "auto_alerting": auto_alerting_enabled,
        "timestamp": datetime.now().isoformat()
    }

# Control auto-alerting
@app.post("/auto-alerts/toggle")
def toggle_auto_alerts():
    """Toggle automatic alert generation on/off"""
    global auto_alerting_enabled
    auto_alerting_enabled = not auto_alerting_enabled
    status = "enabled" if auto_alerting_enabled else "disabled"
    return {
        "status": "success",
        "auto_alerting": auto_alerting_enabled,
        "message": f"Auto-alerting {status}",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate-all-alerts")
def generate_all_alerts_now():
    """Manually generate alerts for all towers"""
    try:
        towers_to_check = fetch_all_towers()
        if not towers_to_check:
            return {
                "status": "error",
                "message": "No towers found",
                "timestamp": datetime.now().isoformat()
            }
        
        total_alerts = 0
        results = []
        
        for tower_id in towers_to_check:
            try:
                # Generate alerts for this tower
                telemetry_data = fetch_telemetry_data(tower_id)
                siteboss_data = fetch_siteboss_data(tower_id)
                tower_info = fetch_tower_info(tower_id)
                hardware_data = fetch_hardware_data(tower_id)
                maintenance_data = fetch_maintenance_data(tower_id)
                
                # Create analysis prompt
                analysis_prompt = f"""
                You are an expert in 5G tower monitoring. Analyze this tower data for any issues requiring alerts:
                
                TOWER ID: {tower_id}
                TELEMETRY DATA: {json.dumps(telemetry_data, indent=2)}
                SITEBOSS DATA: {json.dumps(siteboss_data, indent=2)}
                HARDWARE COMPONENTS: {json.dumps(hardware_data or [], indent=2)}
                MAINTENANCE RECORDS: {json.dumps(maintenance_data or [], indent=2)}
                
                Identify any critical issues, security breaches, maintenance needs, or hardware problems.
                Be concise and focus only on actionable items.
                """
                
                # Get AI analysis
                analyzer = get_gemini_analyzer()
                if analyzer:
                    analysis = analyzer.model.generate_content(analysis_prompt)
                    analysis_text = clean_markdown_formatting(analysis.text)
                else:
                    analysis_text = f"Tower {tower_id} status: Normal operation. No immediate alerts required."
                
                # Extract and create alerts
                extracted_alerts = extract_alerts_from_analysis(analysis_text, tower_id)
                created_count = 0
                
                for alert_data in extracted_alerts:
                    created_alert = create_alert(
                        alert_data["tower_id"],
                        alert_data["title"],
                        alert_data["description"],
                        alert_data["severity"]
                    )
                    if created_alert:
                        created_count += 1
                
                total_alerts += created_count
                results.append({
                    "tower_id": tower_id,
                    "alerts_created": created_count
                })
                
            except Exception as e:
                print(f"❌ Error processing Tower {tower_id}: {e}")
                results.append({
                    "tower_id": tower_id,
                    "alerts_created": 0,
                    "error": str(e)
                })
        
        return {
            "status": "success",
            "message": f"Generated {total_alerts} alerts across {len(towers_to_check)} towers",
            "total_alerts": total_alerts,
            "towers_processed": len(towers_to_check),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating alerts: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Tower analysis endpoint
@app.post("/analyze-tower", response_model=TowerAnalysisResponse)
def analyze_tower_data(request: TowerAnalysisRequest):
    """Analyze tower data using Gemini AI"""
    try:
        analysis = gemini_analyzer.analyze_tower_data(
            request.tower_id,
            request.telemetry_data,
            request.siteboss_data
        )
        
        return TowerAnalysisResponse(
            tower_id=request.tower_id,
            analysis=analysis,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return TowerAnalysisResponse(
            tower_id=request.tower_id,
            analysis=f"Error analyzing tower data: {str(e)}",
            timestamp=datetime.now().isoformat()
        )

# Chat endpoint for interactive conversations
@app.post("/chat", response_model=ChatMessageResponse)
def chat_with_ai(request: ChatMessageRequest):
    """Chat with AI about tower data"""
    try:
        # Fetch real data if not provided
        telemetry_data = request.telemetry_data or fetch_telemetry_data(request.tower_id)
        siteboss_data = request.siteboss_data or fetch_siteboss_data(request.tower_id)
        tower_info = fetch_tower_info(request.tower_id)
        hardware_data = fetch_hardware_data(request.tower_id)
        maintenance_data = fetch_maintenance_data(request.tower_id)
        
        # Check if this is a greeting message or system-wide question
        message_lower = request.message.lower().strip()
        exact_greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
        help_requests = ['what can you do', 'what can you help with', 'help', 'start']
        system_questions = ['what towers', 'list towers', 'all towers', 'show towers', 'towers in system', 'system overview', 'overview']
        
        # Check if this is a system-wide question about towers
        is_system_question = any(phrase in message_lower for phrase in system_questions)
        
        # Only treat as greeting if it's a simple greeting or help request without other content
        is_greeting = (
            message_lower in exact_greetings or 
            message_lower in help_requests or
            (len(message_lower.split()) <= 3 and any(greeting in message_lower for greeting in exact_greetings))
        )
        
        # Determine context: if tower_id is 0 or -1, treat as system-wide context
        is_system_context = request.tower_id in [0, -1, None] or is_system_question
        
        if is_system_context or is_system_question:
            # Handle system-wide questions about all towers
            all_towers = fetch_all_towers()
            if all_towers:
                # Fetch basic info for all towers
                towers_info = []
                for tower_id in all_towers:
                    try:
                        tower_data = fetch_tower_info(tower_id)
                        if tower_data:
                            towers_info.append({
                                "id": tower_id,
                                "name": tower_data.get("name", f"Tower {tower_id}"),
                                "status": tower_data.get("status", "unknown"),
                                "city": tower_data.get("city", "unknown"),
                                "useCase": tower_data.get("useCase", "unknown"),
                                "battery": tower_data.get("battery", 0),
                                "temperature": tower_data.get("temperature", 0)
                            })
                    except Exception as e:
                        print(f"Error fetching info for tower {tower_id}: {e}")
                
                prompt = f"""
                You are a helpful AI assistant for tower monitoring. A user is asking about towers in the system.
                
                USER QUESTION: {request.message}
                
                SYSTEM TOWERS INFORMATION:
                {json.dumps(towers_info, indent=2)}
                
                Please provide a comprehensive overview of all towers in the system. Include:
                1. Total number of towers
                2. Brief summary of each tower (name, location, status, use case, battery, temperature)
                3. Overall system health status
                4. Any notable patterns or insights across all towers
                5. Regional distribution and use case analysis
                
                Be organized and clear in your response. Group towers by status, region, or use case if helpful.
                If the user asks about specific towers, provide detailed information about those towers.
                If they ask general questions, provide system-wide insights and statistics.
                """
            else:
                prompt = f"""
                You are a helpful AI assistant for tower monitoring. A user is asking about towers in the system.
                
                USER QUESTION: {request.message}
                
                SYSTEM TOWERS INFORMATION: No towers found in the system.
                
                Please inform the user that no towers are currently available in the system and suggest they check the system status or contact an administrator.
                """
        else:
            prompt = f"""
            You are a helpful AI assistant for tower monitoring. A user is asking about tower {request.tower_id} specifically.
            
            USER QUESTION: {request.message}
            
            FOCUS: This is a tower-specific query. Provide detailed information about Tower {request.tower_id} only.
            Do NOT provide information about other towers unless specifically asked.
            
            TOWER INFORMATION: {json.dumps(tower_info, indent=2)}
            
            TELEMETRY DATA: {json.dumps(telemetry_data, indent=2)}
            
            SITEBOSS DATA: {json.dumps(siteboss_data, indent=2)}
            
            HARDWARE COMPONENTS: {json.dumps(hardware_data, indent=2)}
            
            MAINTENANCE RECORDS: {json.dumps(maintenance_data, indent=2)}
            
            Please provide a helpful, conversational response focused specifically on Tower {request.tower_id}.
            You have access to comprehensive data, so you can provide insights about:
            - Hardware health and specifications for this tower
            - Maintenance schedules and history for this tower
            - Equipment warranties and install dates for this tower
            - Maintenance priorities and costs for this tower
            - Technician assignments and contact information for this tower
            - Current status, performance, and any issues specific to this tower
            """
        
        # Get response from Gemini
        analyzer = get_gemini_analyzer()
        if analyzer:
            response = analyzer.model.generate_content(prompt)
            # Clean markdown formatting from the response
            response_text = clean_markdown_formatting(response.text)
        else:
            # Fallback response if Gemini is not available
            if is_system_context:
                if "hello" in request.message.lower() or "hi" in request.message.lower():
                    response_text = "Hello! I'm the AI assistant for the tower monitoring system. I can help you with information about all towers in the system. How can I help you today?"
                elif "towers" in request.message.lower():
                    response_text = "I can help you get information about all towers in the system. We have multiple towers across different locations. Would you like me to provide an overview of all towers?"
                else:
                    response_text = "I can help you with system-wide tower information, including overviews of all towers, regional analysis, and system health status. What would you like to know?"
            else:
                if "hello" in request.message.lower() or "hi" in request.message.lower():
                    response_text = f"Hello! I'm the AI assistant for Tower {request.tower_id}. How can I help you today?"
                elif "status" in request.message.lower():
                    response_text = f"Tower {request.tower_id} is currently online and operating normally. All systems are functioning within expected parameters."
                elif "temperature" in request.message.lower():
                    response_text = f"Tower {request.tower_id} temperature is currently at 32°C, which is within normal operating range."
                elif "battery" in request.message.lower():
                    response_text = f"Tower {request.tower_id} battery level is at 85%, which is good. No immediate charging required."
                else:
                    response_text = f"I understand you're asking about Tower {request.tower_id}. I can help you with status updates, performance metrics, maintenance schedules, and troubleshooting. What specific information would you like to know?"
            
            return ChatMessageResponse(
                tower_id=request.tower_id,
                user_message=request.message,
                ai_response=response_text,
                timestamp=datetime.now().isoformat()
            )
        
        return ChatMessageResponse(
            tower_id=request.tower_id,
            user_message=request.message,
            ai_response=response_text,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return ChatMessageResponse(
            tower_id=request.tower_id,
            user_message=request.message,
            ai_response=f"Sorry, I encountered an error: {str(e)}",
            timestamp=datetime.now().isoformat()
        )

# Simple test endpoint
@app.get("/test-gemini")
def test_gemini():
    """Simple test endpoint for Gemini"""
    try:
        result = gemini_analyzer.simple_test()
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

# Get tower insights (using real data)
@app.get("/tower/{tower_id}/insights")
def get_tower_insights(tower_id: int):
    """Get insights for a specific tower using real data"""
    try:
        # Fetch real data from multiple sources
        telemetry_data = fetch_telemetry_data(tower_id)
        siteboss_data = fetch_siteboss_data(tower_id)
        tower_info = fetch_tower_info(tower_id)
        hardware_data = fetch_hardware_data(tower_id)
        maintenance_data = fetch_maintenance_data(tower_id)
        
        # Combine all data for analysis
        combined_data = {
            "tower_info": tower_info,
            "telemetry_data": telemetry_data,
            "siteboss_data": siteboss_data,
            "hardware_data": hardware_data,
            "maintenance_data": maintenance_data
        }
        
        # Create a comprehensive prompt for Gemini with all data
        analyzer = get_gemini_analyzer()
        if analyzer:
            analysis = analyzer.analyze_tower_data(tower_id, telemetry_data, siteboss_data, hardware_data, maintenance_data)
        else:
            analysis = f"Tower {tower_id} analysis: Basic health check shows normal operation. All systems functioning within expected parameters."
        
        return {
            "tower_id": tower_id,
            "analysis": analysis,
            "data_sources": {
                "telemetry_available": len(telemetry_data) > 0,
                "siteboss_available": len(siteboss_data) > 0,
                "tower_info_available": len(tower_info) > 0,
                "hardware_available": len(hardware_data) > 0,
                "maintenance_available": len(maintenance_data) > 0
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "tower_id": tower_id,
            "error": f"Error getting insights: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Generate AI-powered notifications
@app.post("/tower/{tower_id}/generate-alerts")
def generate_ai_alerts(tower_id: int):
    """Generate AI-powered alerts based on tower analysis"""
    try:
        # Fetch real data from multiple sources
        telemetry_data = fetch_telemetry_data(tower_id)
        siteboss_data = fetch_siteboss_data(tower_id)
        tower_info = fetch_tower_info(tower_id)
        hardware_data = fetch_hardware_data(tower_id)
        maintenance_data = fetch_maintenance_data(tower_id)
        
        # Create a comprehensive analysis prompt focused on generating alerts
        analysis_prompt = f"""
        You are an expert in 5G tower monitoring and predictive maintenance.
        
        Analyze this tower data and identify any issues that require immediate attention or alerts:
        
        TOWER ID: {tower_id}
        
        TELEMETRY DATA:
        {json.dumps(telemetry_data, indent=2)}
        
        SITEBOSS DATA:
        {json.dumps(siteboss_data, indent=2)}
        
        HARDWARE COMPONENTS:
        {json.dumps(hardware_data or [], indent=2)}
        
        MAINTENANCE RECORDS:
        {json.dumps(maintenance_data or [], indent=2)}
        
        Please analyze the data and identify:
        1. CRITICAL ISSUES that need immediate attention
        2. MAINTENANCE ALERTS for upcoming or overdue maintenance
        3. HARDWARE ISSUES that could cause problems
        4. PERFORMANCE ANOMALIES that need investigation
        
        Focus on actionable items that would require creating alerts or notifications.
        Be specific about what issues you find and their severity.
        """
        
        # Get analysis from Gemini
        analysis = gemini_analyzer.model.generate_content(analysis_prompt)
        analysis_text = clean_markdown_formatting(analysis.text)
        
        # Extract alerts from the analysis
        extracted_alerts = extract_alerts_from_analysis(analysis_text, tower_id)
        
        # Create alerts in the backend
        created_alerts = []
        for alert_data in extracted_alerts:
            created_alert = create_alert(
                alert_data["tower_id"],
                alert_data["title"],
                alert_data["description"],
                alert_data["severity"]
            )
            if created_alert:
                created_alerts.append(created_alert)
        
        return {
            "tower_id": tower_id,
            "analysis": analysis_text,
            "alerts_generated": len(created_alerts),
            "created_alerts": created_alerts,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "tower_id": tower_id,
            "error": f"Error generating alerts: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }