# 5SKYE Digital Twin Platform - Simple Overview

## What is 5SKYE?

5SKYE is a web application that monitors telecommunication towers. Think of it like a control room where you can:
- See all your towers on a 3D map
- Check their health (battery, temperature, etc.)
- Chat with an AI assistant about tower problems
- Get automatic alerts when something goes wrong

## How It Works

### The Main Parts:

1. **Website (Frontend)** - What users see and click on
2. **Server (Backend)** - Stores tower data and handles requests
3. **AI Service** - The smart chatbot that analyzes tower data
4. **Data Simulator** - Creates fake tower data for testing
5. **Monitoring Tools** - Shows graphs and charts

### Simple Flow:
```
Tower Data → Server → Website → User sees it
     ↓
AI Service analyzes data → Creates alerts → User gets notified
```

## What Users Can Do:

### Main Dashboard:
- See a 3D globe with tower locations
- Click on towers to see details
- View live data (battery, temperature, etc.)

### Tower Details:
- See specific tower information
- Chat with AI about that tower
- View maintenance records
- Access detailed monitoring charts

### AI Chatbot:
- Ask questions about towers
- Get automatic alerts
- Ask for system overviews

## Technical Stuff:

### What's Working:
- ✅ 3D tower map
- ✅ Real-time data display
- ✅ AI chatbot (when API limits allow)
- ✅ Alert system
- ✅ Modern web interface

### Current Limitations:
- ⚠️ AI service hits daily API limits (200 requests/day)
- ⚠️ Some services crash due to code errors
- ⚠️ Performance varies based on data size
- ⚠️ Development environment (not production-ready)

### Technologies Used:
- **Frontend**: React/Next.js (modern web framework)
- **Backend**: Spring Boot (Java server)
- **Database**: PostgreSQL (data storage)
- **AI**: Google Gemini API (chatbot)
- **3D**: CesiumJS (3D globe)
- **Monitoring**: Grafana + Prometheus (charts and metrics)

## Current Status:

This is a **working prototype** that demonstrates:
- Real-time tower monitoring
- AI-powered insights
- 3D visualization
- Alert management

The system works but has limitations due to:
- Free API quotas
- Development environment setup
- Some code stability issues

## For Diagrams:

Use this to create simple diagrams showing:
1. User → Website → Server → Database
2. AI Service → Analyzes Data → Creates Alerts
3. 3D Map → Shows Towers → Real-time Data
4. Monitoring Tools → Charts and Graphs

This gives you the honest, simple truth about what you've built!

