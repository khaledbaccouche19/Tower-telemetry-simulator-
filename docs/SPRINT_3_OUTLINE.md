# Sprint 3: Telemetry Monitoring and Data Ingestion - Detailed Outline

## 4.1.1 Sprint Goals, Backlog, and Technical Objectives

### Sprint Goals
- Enable real-time telemetry ingestion from simulator and external sources
- Implement historical data persistence in PostgreSQL
- Build live telemetry visualization in the frontend
- Expose metrics to Prometheus and configure Grafana dashboards

### Backlog Items
- **F9**: Visualize live telemetry (simulator); prepare SiteBoss integration → **High, L**
- **F10**: Store/analyze historical metrics via Prometheus/Grafana → **High, M**
- **F11**: Integrate Grafana dashboards for visualization → **Medium, S**

### Technical Approach
- Two-tier architecture: Simulator → Backend Proxy → Frontend
- Scheduled ingestion job runs every 30 seconds
- Deduplication prevents duplicate timestamps
- Prometheus metrics for observability

---

## 4.1.2 Telemetry Simulator Architecture and Live Data Source

### Simulator Design
- **Technology**: Spring Boot application running on port 8080
- **Purpose**: Generate realistic tower telemetry data for development/testing
- **Location**: `tower-telemetry-simulator/`

### Key Features
- REST API endpoint: `GET /api/telemetry/live`
- Returns JSON array of telemetry objects
- Generates synthetic but realistic data for multiple towers

### Metric Fields Generated
1. **Environmental**: temperature, ambientTemperature, humidity, windSpeed, windDirection, airQuality, uvIndex, pressure, precipitation
2. **Network**: networkLoad, signalStrength, latency, packetLoss, jitter, bandwidth, throughput, responseTime, interference
3. **System**: cpuUtilization, memoryUsage, diskSpace, errorRate, uptime
4. **Infrastructure**: vibration, voltage, battery, status

### Integration Strategy
- Primary development source during Sprint 3
- Production path: SiteBoss SNMP/REST integration (future sprint)
- Simulator validates end-to-end telemetry flow before real hardware integration

---

## 4.1.3 Backend Telemetry Ingest Service and Historical Persistence

### Core Components

#### TelemetryIngestScheduler
- **Location**: `5skye-backend-main/src/main/java/com/example/demo/service/TelemetryIngestScheduler.java`
- **Scheduling**: `@Scheduled(fixedDelay = 30000, initialDelay = 10000)` - runs every 30 seconds
- **Process**:
  1. Fetch all towers from database
  2. For each tower with valid API endpoint
  3. Make HTTP GET request to telemetry source
  4. Transform response to DTO format
  5. Persist via TelemetryDataService
  6. Export metrics to Prometheus

#### Deduplication Logic
```java
// Simple dedupe: skip if an entry already exists with same towerId and timestamp
boolean exists = !telemetryDataRepository
    .findByTowerIdAndTimestampBetweenOrderByTimestampAsc(towerId, dto.getTimestamp(), dto.getTimestamp())
    .isEmpty();
if (!exists) {
    telemetryDataService.createTelemetryData(dto);
    meterRegistry.counter("telemetry_ingest_saved_total", "towerId", String.valueOf(towerId)).increment();
}
```

#### Database Schema
- **Entity**: `TelemetryData` in PostgreSQL
- **Fields**: towerId, timestamp, status, battery, uptime, temperature, ambientTemperature, humidity, windSpeed, windDirection, airQuality, uvIndex, pressure, precipitation, networkLoad, signalStrength, latency, packetLoss, jitter, bandwidth, throughput, responseTime, interference, cpuUtilization, memoryUsage, diskSpace, errorRate, vibration, voltage

#### REST API Endpoints
- `GET /api/telemetry/tower/{id}` - Historical telemetry data for a specific tower
- Proxy endpoint for live telemetry data (fetches from simulator/external source)

---

## 4.1.4 Real-Time Telemetry Visualization in Frontend

### Data Flow
1. Frontend calls `ApiClient.fetchTelemetryData(towerId)`
2. Backend proxies request to simulator (port 8080)
3. Backend transforms and returns data to frontend
4. Frontend updates UI components with latest values

### Key Implementation Details

#### Auto-Refresh Mechanism
```typescript
// Periodic refresh every 30 seconds (configurable)
useEffect(() => {
  fetchTowers()
  const intervalId = setInterval(() => {
    fetchTowers()
  }, 30000)
  return () => clearInterval(intervalId)
}, [])
```

#### UI Components
- **Metric Cards**: Display battery, temperature, uptime, network load
- **Status Indicators**: Visual health indicators (green/yellow/red)
- **Last Update Timestamp**: Show when data was last refreshed
- **Historical Charts**: Time-series visualization of stored telemetry

#### Error Handling
- Graceful degradation when simulator unavailable
- Warning logs instead of blocking errors
- Falls back to stored historical data if live data unavailable

### Pages Using Telemetry
1. **Dashboard** (`/`): Tower overview with live metrics
2. **Towers List** (`/towers`): Live data for all towers, auto-refresh every 30s
3. **Tower Detail** (`/towers/[id]`): Comprehensive live + historical telemetry view

---

## 4.1.5 Prometheus Metrics Exposure and Grafana Configuration

### Metrics Integration

#### Micrometer Integration
- Backend uses Micrometer for metrics collection
- Automatic timer registration for ingest jobs
- Custom counters for success/failure tracking

#### Key Metrics Exposed
1. `telemetry_ingest_duration_seconds` - Duration of ingestion job execution
2. `telemetry_ingest_runs_total` - Total number of ingest runs
3. `telemetry_ingest_errors_total` - Count of errors per tower
4. `telemetry_ingest_saved_total` - Count of successfully saved data points
5. `simulator_metric_value` - Dynamic gauges for latest telemetry values
   - Tags: towerId, metric_type, unit
   - Metrics: temperature, ambient_temperature, humidity, battery, network_load, uptime, wind_speed, signal_strength, latency, packet_loss, jitter, bandwidth, throughput, response_time, cpu_utilization

### Prometheus Configuration
- **Endpoint**: `GET /actuator/prometheus` on port 8088
- **Scrape interval**: Configured in `prometheus.yml` (typically 15-30s)
- **Metrics format**: Prometheus text-based exposition format

### Grafana Dashboard
- **Location**: `grafana/dashboards/5sky-complete-monitoring-dashboard.json`
- **Panels**:
  1. Ingest job duration over time
  2. Ingest run counter (cumulative)
  3. Error rate per tower
  4. Latest telemetry values per metric type
  5. Historical trends for key metrics
- **Provisioning**: Docker Compose sets up dashboard automatically

---

## 4.1.6 In-App Monitoring Experience and Embedded Dashboards

### Monitoring Page
- Dedicated monitoring view showing system health
- Embed Grafana panels or standalone metrics display
- Real-time updates from Prometheus data

### Performance Analysis
- Ingest duration tracking
- Error rates per tower
- Data freshness indicators
- System load metrics

### Integration with Tower Detail Pages
- Real-time telemetry display
- Historical chart visualization
- Toggle between live and stored data views

### User Controls
- Enable/disable auto-refresh
- Adjust polling interval
- Manual refresh button
- Data export functionality

---

## 4.1.7 Sprint Outcomes, Performance Evaluation, and Retrospective

### Achievements ✅
1. Live telemetry pipeline fully operational
2. Historical data storage functional with deduplication
3. Prometheus metrics exposed and queryable
4. Grafana dashboards provisioned and functional
5. Frontend displays real-time data with auto-refresh

### Performance Metrics
- **Ingest duration**: 50-200ms per tower (typical)
- **Ingest cadence**: Every 30 seconds
- **Database writes**: Optimized with timestamp-based deduplication
- **API response time**: <100ms for proxy requests
- **Frontend refresh**: Non-blocking, graceful degradation

### Challenges Encountered
1. **Simulator stability**: Occasional crashes requiring restart
2. **Data consistency**: Need to handle race conditions in concurrent updates
3. **Memory management**: Gauges can accumulate if not properly managed
4. **Error propagation**: Balancing logging vs user experience

### Lessons Learned
1. **Proxy pattern**: Centralizing backend proxy reduces frontend complexity
2. **Deduplication critical**: Prevents database bloat and query slowdown
3. **Metrics first**: Micrometer integration provides immediate observability value
4. **Graceful degradation**: Frontend should continue working even if telemetry fails

### Evidence to Collect
1. Screenshot of live telemetry on tower detail page
2. Grafana dashboard showing ingest metrics
3. Sample API response from simulator endpoint
4. Database query showing historical data
5. Prometheus metrics output showing gauge values
6. Error log demonstrating deduplication working

### Technical Debt / Future Improvements
1. Add retry logic for transient telemetry fetch failures
2. Implement data retention policy for historical telemetry
3. Add compression for high-frequency metrics
4. Optimize gauge cleanup to prevent memory leaks
5. SiteBoss SNMP integration for production data sources

---

## Code References

### Backend
- `TelemetryIngestScheduler.java` - Main ingest job
- `TelemetryDataService.java` - Service layer for persistence
- `TelemetryDataController.java` - REST API endpoints
- `TelemetryDataRepository.java` - Database access
- `application.properties` - Scheduler configuration

### Frontend
- `app/towers/[id]/page.tsx` - Tower detail with telemetry display
- `app/towers/page.tsx` - Towers list with live data
- `app/page.tsx` - Dashboard with telemetry overview
- `lib/api-client.ts` - API client with telemetry methods

### Configuration
- `docker-compose.observability.yml` - Prometheus + Grafana setup
- `grafana/dashboards/5sky-complete-monitoring-dashboard.json` - Dashboard definition
- `prometheus_siteboss.yml` - Prometheus scrape configuration


