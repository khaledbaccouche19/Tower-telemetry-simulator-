# Tower Telemetry Simulator

A Spring Boot application that simulates live telemetry data for a single telecommunications tower with comprehensive frontend integration support.

## Features

- **REST API endpoints** for live telemetry data and historical analysis
- **Simulated data for 1 tower** (Main Tower) with realistic operational metrics
- **Realistic data ranges** for telecommunications equipment and environmental conditions
- **Historical data generation** with configurable time ranges (1h, 24h, 7d, 30d)
- **Tower summary and metadata** for dashboard integration
- **CORS enabled** for frontend integration on ports 3000/3001
- **Data updates on each API call** for real-time simulation

## API Endpoints

### **Live Telemetry Data**
- `GET /api/telemetry/live` - Returns live telemetry data for the main tower

### **Historical Data**
- `GET /api/telemetry/tower/1/history?timeRange=24h` - Historical data for the main tower
  - **timeRange options**: `1h`, `24h`, `7d`, `30d` (default: `24h`)

### **Tower Information**
- `GET /api/towers/summaries` - Dashboard summary for the main tower
- `GET /api/towers` - Complete tower information including coordinates

### **Health Check**
- `GET /api/telemetry/health` - Health check endpoint

## Data Fields

### **System Health Metrics**
- **Battery**: 80-100%
- **Temperature**: 35-50°C
- **Uptime**: 99.0-100.0%
- **Network Load**: 50-90%
- **CPU Utilization**: 30-80%
- **Memory Usage**: 60-90%
- **Disk Space**: 50-90%
- **Voltage**: 12.0-13.0V

### **Network Performance**
- **Signal Strength**: -70 to -50 dBm
- **Response Time**: 20-50ms
- **Throughput**: 500-1000 Mbps
- **Bandwidth**: 100-1000 Mbps
- **Latency**: 15-40ms
- **Jitter**: 2-10ms
- **Packet Loss**: 0-0.2%
- **Error Rate**: 0-0.1%
- **Interference**: 5-25

### **Environmental Conditions**
- **Ambient Temperature**: 20-40°C
- **Humidity**: 40-80%
- **Wind Speed**: 5-30 km/h
- **Wind Direction**: N, NE, E, SE, S, SW, W, NW
- **Air Quality**: 70-95
- **UV Index**: 1-11
- **Precipitation**: 0-5mm
- **Pressure**: 1000-1040 hPa
- **Vibration**: 0-0.5

## Response Format Examples

### **Live Telemetry Data**
```json
[
  {
    "towerId": 1,
    "towerName": "Main Tower",
    "timestamp": "2025-01-16T15:30:00Z",
    "battery": 87.0,
    "temperature": 42.0,
    "uptime": 99.8,
    "networkLoad": 73.0,
    "ambientTemperature": 32.0,
    "humidity": 58.0,
    "windSpeed": 18.0,
    "airQuality": 85.0,
    "signalStrength": -62.0,
    "cpuUtilization": 45.0,
    "memoryUsage": 76.0,
    "voltage": 12.4,
    "responseTime": 35.2,
    "throughput": 723.8,
    "diskSpace": 67.3,
    "errorRate": 0.03,
    "interference": 12.7,
    "packetLoss": 0.08,
    "latency": 28.5,
    "jitter": 4.2,
    "bandwidth": 456.8,
    "vibration": 0.23,
    "windDirection": "NE",
    "uvIndex": 7.8,
    "precipitation": 1.2,
    "pressure": 1015.6
  }
]
```

### **Tower Summary**
```json
[
  {
    "id": 1,
    "name": "Main Tower",
    "status": "online",
    "battery": 87.5,
    "temperature": 42.3,
    "uptime": 99.8,
    "networkLoad": 73.2,
    "city": "Main Location",
    "region": "Primary Region",
    "useCase": "Core Network",
    "lastMaintenance": "2024-12-17T10:30:00"
  }
]
```

### **Tower Information**
```json
[
  {
    "id": 1,
    "name": "Main Tower",
    "status": "online",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "city": "Main Location",
    "useCase": "Core Network",
    "region": "Primary Region",
    "model3dPath": null,
    "createdAt": "2024-12-17T10:30:00",
    "updatedAt": "2025-01-16T15:30:00"
  }
]
```

## Running the Application

### Prerequisites
- Java 17 or higher
- Maven 3.6 or higher

### Build and Run
```bash
# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

The application will start on **port 8080**.

### Test the API
```bash
# Test live telemetry endpoint
curl http://localhost:8080/api/telemetry/live

# Test historical data endpoint
curl http://localhost:8080/api/telemetry/tower/1/history?timeRange=24h

# Test tower summaries endpoint
curl http://localhost:8080/api/towers/summaries

# Test all towers endpoint
curl http://localhost:8080/api/towers

# Test health endpoint
curl http://localhost:8080/api/telemetry/health
```

## Configuration

- **Port**: 8080 (configurable in application.properties)
- **Database**: H2 in-memory database
- **CORS**: Enabled for ports 3000 and 3001 (frontend development)

## Project Structure

```
src/main/java/com/example/telemetry/
├── TowerTelemetrySimulatorApplication.java  # Main application class
├── TelemetryData.java                       # Enhanced data model with all fields
├── TelemetryController.java                 # REST controller with new endpoints
├── TelemetrySimulationService.java          # Enhanced data generation service
├── TowerSummary.java                        # Dashboard summary data model
├── Tower.java                               # Tower metadata model
├── DataRetentionService.java                # Data storage and retention service
└── CorsConfig.java                          # CORS configuration

src/main/resources/
└── application.properties                   # Configuration file
```

## Frontend Integration

The API is configured with CORS enabled for ports 3000 and 3001, making it perfect for frontend development. 

### **Integration Examples**

#### **Live Data Updates**
```javascript
// Poll every 5 seconds for live updates
setInterval(async () => {
  const response = await fetch('http://localhost:8080/api/telemetry/live');
  const liveData = await response.json();
  updateDashboard(liveData[0]); // Single tower data
}, 5000);
```

#### **Historical Data for Charts**
```javascript
// Get 24-hour historical data for charts
const response = await fetch('http://localhost:8080/api/telemetry/tower/1/history?timeRange=24h');
const historicalData = await response.json();
renderChart(historicalData);
```

#### **Tower Summary for Dashboard**
```javascript
// Get tower summary for dashboard overview
const response = await fetch('http://localhost:8080/api/towers/summaries');
const summaries = await response.json();
updateTowerCard(summaries[0]); // Single tower summary
```

### **Real-time Updates**
For real-time updates, poll the live endpoint every 5 seconds or implement WebSocket connections for more efficient real-time communication.

## Data Simulation

The application generates realistic telemetry data with each API call, ensuring:
- **Varied data ranges** within realistic bounds
- **Consistent data patterns** for the single tower
- **Time-based historical data** for trend analysis
- **Environmental correlation** between related metrics

This makes it perfect for:
- **Development & Testing** of single tower monitoring dashboards
- **Frontend Prototyping** with realistic data
- **Demo & Presentations** of telemetry systems
- **Training & Learning** about IoT/telemetry data structures
