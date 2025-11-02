import google.generativeai as genai
import json
from typing import Dict, List, Any

class GeminiTowerAnalyzer:
    def __init__(self, api_key: str):
        """Initialize Gemini with API key"""
        genai.configure(api_key=api_key)
        # Use the working model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def analyze_tower_data(self, tower_id: int, telemetry_data: List[Dict], siteboss_data: Dict, hardware_data: List[Dict] = None, maintenance_data: List[Dict] = None) -> str:
        """Analyze tower data using Gemini"""
        
        # Create the prompt for Gemini
        prompt = f"""
        You are an expert in 5G tower monitoring and predictive maintenance.
        
        Analyze this tower data and provide comprehensive insights:
        
        TOWER ID: {tower_id}
        
        TELEMETRY DATA:
        {json.dumps(telemetry_data, indent=2)}
        
        SITEBOSS DATA:
        {json.dumps(siteboss_data, indent=2)}
        
        HARDWARE COMPONENTS:
        {json.dumps(hardware_data or [], indent=2)}
        
        MAINTENANCE RECORDS:
        {json.dumps(maintenance_data or [], indent=2)}
        
        Please provide your analysis in this format:
        
        1. OVERALL HEALTH SCORE (1-10)
        2. CRITICAL ISSUES FOUND
        3. HARDWARE COMPONENT STATUS
        4. MAINTENANCE RECOMMENDATIONS
        5. PRIORITY LEVEL (LOW/MEDIUM/HIGH/CRITICAL)
        6. NEXT ACTIONS REQUIRED
        7. EQUIPMENT LIFECYCLE INSIGHTS
        
        Be specific and actionable in your recommendations.
        Focus on immediate concerns, predictive maintenance needs, hardware health, and maintenance scheduling.
        """
        
        try:
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error analyzing tower data: {str(e)}"
    
    def simple_test(self) -> str:
        """Simple test function"""
        try:
            response = self.model.generate_content("Hello! Can you analyze tower monitoring data?")
            return response.text
        except Exception as e:
            return f"Error in simple test: {str(e)}"

# Example usage
if __name__ == "__main__":
    # You'll need to add your API key here
    api_key = "AIzaSyAJ5NnpeZp0QbCej8EgbGJa8jGzdLF0fDo"
    analyzer = GeminiTowerAnalyzer(api_key)
    
    # Test with sample data
    sample_telemetry = [
        {"battery": 85, "temperature": 32, "uptime": 99.8, "networkLoad": 45},
        {"battery": 84, "temperature": 33, "uptime": 99.7, "networkLoad": 46}
    ]
    
    sample_siteboss = {
        "sensors": [
            {"name": "Temperature", "value": "32°C", "status": "normal"},
            {"name": "Power", "value": "12.3V", "status": "warning"}
        ]
    }
    
    # Uncomment to test
    # result = analyzer.analyze_tower_data(49, sample_telemetry, sample_siteboss)
    # print(result)
