# 5SKYE Digital Twin Platform - Complete Architecture Documentation

## 🏗️ Project Overview

The 5SKYE Digital Twin Platform is a web-based system for telecommunication tower monitoring that combines real-time data, AI analytics, 3D visualization, and alerting. It provides a virtual interface for monitoring telecommunication infrastructure with data visualization and AI-powered insights.

---

## 🎯 Core Components & Architecture

### 1. Frontend Layer (Next.js/React)
- **Framework**: Next.js 14 with TypeScript
- **UI Library**: Tailwind CSS + shadcn/ui components
- **3D Visualization**: CesiumJS for interactive tower mapping
- **State Management**: React Context + useState/useEffect
- **Port**: 3000

#### Key Frontend Features:
- Interactive 3D globe with tower locations
- Real-time dashboard with live metrics
- AI chatbot interface (tower-specific & system-wide)
- Responsive design with glassmorphism UI
- Collapsible sidebar navigation with hover expansion
- Real-time notifications system with alert bell
- Context-aware UI that adapts to user queries

#### Main UI Components:
- **Dashboard Page**: 3D globe view with tower cards showing live metrics
- **Tower Details Page**: Individual tower monitoring with AI chatbot
- **AI Analytics Page**: System-wide analytics and insights
- **Monitoring Page**: Grafana dashboard integration
- **Navigation**: Collapsible sidebar with smooth animations

### 2. Backend Layer (Spring Boot)
- **Framework**: Spring Boot 3.x with Java 17
- **Database**: PostgreSQL for persistent storage
- **Architecture**: RESTful APIs with microservices pattern
- **Port**: 8088

#### Key Backend Services:
- **Tower Management Service**: CRUD operations for tower data
- **Alert Management Service**: Real-time alert creation and tracking
- **Hardware Management Service**: Component tracking and lifecycle
- **Maintenance Management Service**: Scheduling and record keeping
- **SiteBoss Integration Service**: External sensor data ingestion
- **Authentication Service**: JWT-based security

#### Database Schema:
- **Towers Table**: Basic tower information (ID, name, location, status, city, useCase)
- **Alerts Table**: Alert management with severity and resolution tracking
- **Hardware Table**: Component tracking with lifecycle management
- **Maintenance Table**: Scheduling and record keeping
- **Users Table**: Authentication and authorization

### 3. Telemetry Simulator (Spring Boot)
- **Purpose**: Generates realistic tower telemetry data
- **Framework**: Spring Boot with Java
- **Port**: 8080
- **Output**: Prometheus-compatible metrics

#### Data Types Generated:
- Battery level (0-100%)
- Temperature readings (°C)
- System uptime percentage
- Network load percentage
- CPU usage metrics
- Memory usage metrics
- Voltage readings
- Signal strength indicators

#### Features:
- Realistic data patterns with configurable parameters
- Continuous data generation
- Prometheus metrics endpoint
- Configurable simulation parameters

### 4. AI Analytics Service (FastAPI/Python)
- **Framework**: FastAPI with Python 3.9
- **AI Integration**: Google Gemini API (gemini-2.0-flash)
- **Port**: 8000

#### Key AI Features:
- **Context-aware Chatbot**: Tower-specific vs system-wide responses
- **Automatic Alert Generation**: Every 5 minutes for all towers (currently hitting Gemini API quota limits)
- **Multi-data Analysis**: Telemetry + SiteBoss + hardware + maintenance
- **Intelligent Deduplication**: Prevents duplicate alerts
- **LLM-powered Insights**: Analysis using Google Gemini API (free tier with 200 requests/day limit)

#### AI Service Endpoints:
- `/chat`: Interactive chatbot for tower queries
- `/tower/{id}/insights`: Detailed tower analysis
- `/generate-all-alerts`: Manual alert generation for all towers
- `/auto-alerts/toggle`: Control automatic alerting

### 5. Monitoring Stack
- **Prometheus**: Metrics collection and alerting (Port 9090)
- **Grafana**: Visualization dashboards (Port 3001)
- **Integration**: Custom dashboards with tower-specific metrics

#### Monitoring Features:
- Real-time metrics collection
- Custom Grafana dashboards
- Alert rule configuration
- Performance monitoring
- System health tracking

---

## 🔄 Data Flow Architecture

### Real-time Data Pipeline
```
Physical Towers → SiteBoss Sensors → Backend API → Frontend Dashboard
                     ↓
Telemetry Simulator → Prometheus → Grafana → Frontend Metrics
                     ↓
AI Service ← Backend Data ← All Data Sources
```

### AI Processing Flow
```
1. Data Collection: Fetch from all sources (telemetry, SiteBoss, hardware, maintenance)
2. AI Analysis: Gemini processes data for insights
3. Alert Generation: Extract actionable alerts
4. Deduplication: Check existing alerts to prevent spam
5. Backend Storage: Create alerts in PostgreSQL
6. Frontend Display: Real-time notifications in UI
```

### Service Communication Flow
```
Frontend (3000) → Backend API (8088) → PostgreSQL
Frontend (3000) → AI Service (8000) → Gemini API
Frontend (3000) → Grafana (3001) → Prometheus (9090) → Simulator (8080)
AI Service (8000) → Backend API (8088) → All Data Sources
```

---

## 🎨 User Interface Components

### Main Dashboard Features
- **3D Globe**: Interactive CesiumJS map with tower markers
- **Tower Cards**: Live metrics display (battery, temperature, uptime, network)
- **Navigation**: Collapsible sidebar with hover expansion
- **Notifications**: Real-time alert bell with unread count
- **Glassmorphism Design**: Modern UI with transparency effects

### Tower Details Page Components
- **Live Metrics Section**: Real-time telemetry display
- **Real-time Data Section**: SiteBoss sensor information
- **AI Analytics Section**: Context-aware chatbot for tower-specific queries
- **Detailed Information Section**: Hardware specs, maintenance records
- **Grafana Integration**: Direct links to detailed dashboards

### AI Analytics Page Features
- **System-wide Chatbot**: General tower system queries
- **Welcome Interface**: Capability overview and suggestions
- **Context Switching**: Automatic detection of query type
- **Interactive Chat Interface**: Real-time conversation with AI

---

## 🤖 AI Features & Capabilities

### Conversational AI
- **Tower-specific Analysis**: Detailed analysis of individual towers
- **System-wide Overview**: Fleet management and multi-tower insights
- **Context Detection**: Automatic switching based on query type
- **Data Integration**: Access to telemetry, SiteBoss, hardware, maintenance data

### Automated Monitoring
- **5-minute Cycles**: Continuous analysis of all towers (limited by Gemini API quota)
- **Smart Alerting**: Extracts actionable insights from AI analysis
- **Deduplication**: Prevents notification spam
- **Multi-severity Levels**: Critical, High, Medium, Low alert classifications

### Data Sources Integration
- **Telemetry Data**: Battery, temperature, uptime, network load
- **SiteBoss Sensors**: Environmental and security sensors
- **Hardware Components**: Equipment specs, warranties, install dates
- **Maintenance Records**: Schedules, costs, technician assignments

### AI Response Types
- **Greeting Responses**: Welcome messages and capability overviews
- **Tower-specific Queries**: Detailed analysis of individual tower data
- **System-wide Queries**: Overview of all towers and fleet management
- **Maintenance Insights**: Hardware health and maintenance recommendations
- **Performance Analysis**: Operational metrics and trend analysis

---

## 🔧 Technical Implementation Details

### API Endpoints Structure

#### Backend API Endpoints (Port 8088):
- `GET /api/towers`: Retrieve all towers
- `GET /api/towers/{id}`: Get specific tower details
- `GET /api/alerts`: Get all alerts
- `POST /api/alerts`: Create new alert
- `GET /api/hardware/tower/{id}`: Get hardware components for tower
- `GET /api/maintenance/tower/{id}`: Get maintenance records for tower
- `GET /api/siteboss/latest`: Get latest SiteBoss data

#### AI Service Endpoints (Port 8000):
- `POST /chat`: Interactive chatbot endpoint
- `GET /tower/{id}/insights`: Detailed tower analysis
- `POST /generate-all-alerts`: Manual alert generation
- `POST /auto-alerts/toggle`: Control automatic alerting
- `GET /`: Health check endpoint

#### Simulator Endpoints (Port 8080):
- `GET /api/telemetry/live`: Live telemetry data
- Prometheus metrics endpoint for monitoring

### Authentication & Security
- **JWT-based Authentication**: Secure API access
- **CORS Configuration**: Cross-origin request handling
- **Environment Variables**: Secure API key management
- **API Key Protection**: Gemini API key secured in environment

### Database Configuration
- **PostgreSQL**: Primary database for persistent storage
- **Connection Pooling**: Efficient database connections
- **Transaction Management**: ACID compliance for data integrity
- **Indexing**: Optimized queries for performance

---

## 📊 Monitoring & Observability

### Metrics Collection
- **Application Metrics**: Micrometer integration with Spring Boot
- **System Metrics**: CPU, memory, network usage
- **Business Metrics**: Tower health, alert counts, response times
- **Custom Metrics**: Tower-specific performance indicators

### Dashboard Integration
- **Grafana Dashboards**: Custom tower monitoring views
- **Real-time Updates**: Live data refresh every 30 seconds
- **Alert Visualization**: Severity-based color coding
- **Performance Monitoring**: System health and response times

### Logging and Debugging
- **Structured Logging**: Comprehensive application logs
- **Error Tracking**: Detailed error reporting and debugging
- **Performance Monitoring**: Response time tracking
- **AI Service Logging**: Chat interactions and analysis logs

---

## 🚀 Deployment Architecture

### Development Environment
- **Local Services**: All components running locally
- **Port Distribution**: 
  - Frontend: 3000
  - Backend: 8088
  - AI Service: 8000
  - Simulator: 8080
  - Prometheus: 9090
  - Grafana: 3001

### Service Dependencies
```
Frontend → Backend API → PostgreSQL
Frontend → AI Service → Gemini API
Frontend → Grafana → Prometheus → Simulator
AI Service → Backend API → All Data Sources
```

### Environment Configuration
- **Development**: Local development with hot reload
- **Testing**: Automated testing environment
- **Production**: Scalable production deployment (planned)

---

## 🔄 System Workflows

### Tower Monitoring Workflow
1. **Data Collection**: Continuous telemetry and sensor data gathering
2. **Data Processing**: Real-time analysis and metric calculation
3. **Storage**: Persistent storage in PostgreSQL
4. **Visualization**: Real-time display in frontend dashboard
5. **Alerting**: AI-powered anomaly detection and alert generation

### AI Analysis Workflow
1. **Data Aggregation**: Collect data from all sources
2. **Context Determination**: Identify query type (tower-specific vs system-wide)
3. **AI Processing**: Gemini API analysis and insights generation
4. **Response Generation**: Contextual response based on analysis
5. **Alert Extraction**: Identify actionable insights for alerting

### Alert Management Workflow
1. **Continuous Monitoring**: 5-minute automated analysis cycles
2. **Anomaly Detection**: AI-powered issue identification
3. **Alert Generation**: Create actionable alerts with severity levels
4. **Deduplication**: Prevent duplicate alerts for same issues
5. **Notification**: Real-time alert display in frontend UI

---

## 📈 Performance Characteristics

### Response Times
- **Frontend Loading**: Variable depending on network and data size
- **API Responses**: Variable, some endpoints may timeout
- **AI Analysis**: 1-3 seconds when Gemini API is available, longer when quota exceeded
- **Real-time Updates**: 30-second refresh intervals

### Scalability Features
- **Microservices Architecture**: Independent service scaling (planned)
- **Database Optimization**: Basic queries implemented
- **Caching**: Limited caching implemented
- **Load Balancing**: Not currently implemented

### Resource Usage
- **Memory**: Optimized for efficient memory usage
- **CPU**: Lightweight services with minimal overhead
- **Network**: Efficient data transfer and compression
- **Storage**: Optimized database storage and cleanup

---

## 🔧 Development Tools & Environment

### IDEs and Editors
- **IntelliJ IDEA**: Java/Spring Boot development
- **Visual Studio Code**: Frontend and Python development
- **PyCharm**: Python AI service development

### Version Control
- **Git**: Source code version control
- **GitHub**: Repository hosting and collaboration

### Build Tools
- **Maven**: Java/Spring Boot project management
- **npm/pnpm**: Node.js package management
- **pip**: Python package management

### Testing Framework
- **JUnit**: Java unit testing
- **Jest**: JavaScript/TypeScript testing
- **pytest**: Python testing framework

---

## 📋 Project Structure

```
5SKYE-Project/
├── 5skye-Frontend-main/          # Next.js Frontend
│   ├── app/                      # App router pages
│   ├── components/               # React components
│   ├── lib/                      # Utility libraries
│   └── public/                   # Static assets
├── 5skye-backend-main/           # Spring Boot Backend
│   ├── src/main/java/           # Java source code
│   ├── src/main/resources/      # Configuration files
│   └── target/                   # Build artifacts
├── ai-service/                   # Python AI Service
│   ├── app.py                    # FastAPI application
│   ├── gemini_integration.py     # Gemini API integration
│   └── venv/                     # Python virtual environment
├── tower-telemetry-simulator/    # Telemetry Simulator
│   ├── src/main/java/           # Java source code
│   └── target/                   # Build artifacts
└── monitoring/                   # Monitoring configuration
    ├── prometheus.yml            # Prometheus configuration
    └── grafana/                  # Grafana dashboards
```

---

## 🎯 Key Features Summary

### Core Functionality
- ✅ Real-time tower monitoring and visualization
- ✅ 3D interactive globe with tower mapping
- ✅ AI-powered conversational interface (with quota limitations)
- ✅ Automatic alert generation and management (limited by API quotas)
- ✅ Multi-source data integration
- ✅ Responsive web interface with modern UI
- ✅ Basic monitoring and observability

### Advanced Features
- ✅ Context-aware AI responses
- ✅ Intelligent alert deduplication
- ✅ Real-time notification system
- ✅ Hardware and maintenance tracking
- ✅ Grafana dashboard integration
- ✅ Automated monitoring cycles (when API quotas allow)
- ✅ Multi-tower fleet management

### Technical Implementation
- ✅ Basic microservices architecture
- ✅ RESTful API design
- ✅ Modern web technologies
- ⚠️ Basic error handling (some services may crash)
- ⚠️ Basic security practices (development environment)
- ⚠️ Basic design patterns
- ⚠️ Limited performance optimization

This documentation provides a complete technical overview of the 5SKYE Digital Twin Platform, enabling accurate diagram creation for project reports and technical documentation.
