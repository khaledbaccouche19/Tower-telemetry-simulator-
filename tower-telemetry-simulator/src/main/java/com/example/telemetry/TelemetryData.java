package com.example.telemetry;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.math.RoundingMode;

@Entity
@Table(name = "telemetry_data")
public class TelemetryData {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long towerId;
    private String towerName;
    private String status;
    private String timestamp;
    private Double battery;
    private Double temperature;
    private Double uptime;
    private Double networkLoad;
    private Double ambientTemperature;
    private Double humidity;
    private Double windSpeed;
    private Double airQuality;
    private Double signalStrength;
    private Double cpuUtilization;
    private Double memoryUsage;
    
    // NEW FIELDS for frontend integration
    private Double voltage;           // 12.0-13.0V
    private Double responseTime;      // 20-50ms  
    private Double throughput;        // 500-1000 Mbps
    private Double diskSpace;         // 50-90%
    private Double errorRate;         // 0-0.1%
    private Double interference;      // 5-25
    private Double packetLoss;        // 0-0.2%
    private Double latency;           // 15-40ms
    private Double jitter;            // 2-10ms
    private Double bandwidth;         // 100-1000 Mbps
    private Double vibration;         // 0-0.5
    private String windDirection;     // N, NE, E, SE, S, SW, W, NW
    private Double uvIndex;           // 1-11
    private Double precipitation;     // 0-5mm
    private Double pressure;          // 1000-1040 hPa
    
    // Default constructor
    public TelemetryData() {}
    
    // Constructor with parameters
    public TelemetryData(Long towerId, String towerName, String timestamp, Double battery, 
                        Double temperature, Double uptime, Double networkLoad, Double ambientTemperature,
                        Double humidity, Double windSpeed, Double airQuality, Double signalStrength,
                        Double cpuUtilization, Double memoryUsage, Double voltage, Double responseTime,
                        Double throughput, Double diskSpace, Double errorRate, Double interference,
                        Double packetLoss, Double latency, Double jitter, Double bandwidth,
                        Double vibration, String windDirection, Double uvIndex, Double precipitation,
                        Double pressure) {
        this.towerId = towerId;
        this.towerName = towerName;
        this.timestamp = timestamp;
        this.battery = battery;
        this.temperature = temperature;
        this.uptime = uptime;
        this.networkLoad = networkLoad;
        this.ambientTemperature = ambientTemperature;
        this.humidity = humidity;
        this.windSpeed = windSpeed;
        this.airQuality = airQuality;
        this.signalStrength = signalStrength;
        this.cpuUtilization = cpuUtilization;
        this.memoryUsage = memoryUsage;
        this.voltage = voltage;
        this.responseTime = responseTime;
        this.throughput = throughput;
        this.diskSpace = diskSpace;
        this.errorRate = errorRate;
        this.interference = interference;
        this.packetLoss = packetLoss;
        this.latency = latency;
        this.jitter = jitter;
        this.bandwidth = bandwidth;
        this.vibration = vibration;
        this.windDirection = windDirection;
        this.uvIndex = uvIndex;
        this.precipitation = precipitation;
        this.pressure = pressure;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Long getTowerId() { return towerId; }
    public void setTowerId(Long towerId) { this.towerId = towerId; }
    
    public String getTowerName() { return towerName; }
    public void setTowerName(String towerName) { this.towerName = towerName; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    
    public Double getBattery() { return battery; }
    public Double getTemperature() { return temperature; }
    public Double getUptime() { return uptime; }
    public Double getNetworkLoad() { return networkLoad; }
    public Double getAmbientTemperature() { return ambientTemperature; }
    public Double getHumidity() { return humidity; }
    public Double getWindSpeed() { return windSpeed; }
    public Double getAirQuality() { return airQuality; }
    public Double getSignalStrength() { return signalStrength; }
    public Double getCpuUtilization() { return cpuUtilization; }
    public Double getMemoryUsage() { return memoryUsage; }
    
    // NEW GETTERS
    public Double getVoltage() { return voltage; }
    public Double getResponseTime() { return responseTime; }
    public Double getThroughput() { return throughput; }
    public Double getDiskSpace() { return diskSpace; }
    public Double getErrorRate() { return errorRate; }
    public Double getInterference() { return interference; }
    public Double getPacketLoss() { return packetLoss; }
    public Double getLatency() { return latency; }
    public Double getJitter() { return jitter; }
    public Double getBandwidth() { return bandwidth; }
    public Double getVibration() { return vibration; }
    public String getWindDirection() { return windDirection; }
    public Double getUvIndex() { return uvIndex; }
    public Double getPrecipitation() { return precipitation; }
    public Double getPressure() { return pressure; }
    
    // Utility method to format numbers to 2 decimal places
    private Double formatToTwoDecimals(Double value) {
        if (value == null) return null;
        return BigDecimal.valueOf(value).setScale(2, RoundingMode.HALF_UP).doubleValue();
    }
    
    // Override setters to format values to 2 decimal places
    public void setBattery(Double battery) { this.battery = formatToTwoDecimals(battery); }
    public void setTemperature(Double temperature) { this.temperature = formatToTwoDecimals(temperature); }
    public void setUptime(Double uptime) { this.uptime = formatToTwoDecimals(uptime); }
    public void setNetworkLoad(Double networkLoad) { this.networkLoad = formatToTwoDecimals(networkLoad); }
    public void setAmbientTemperature(Double ambientTemperature) { this.ambientTemperature = formatToTwoDecimals(ambientTemperature); }
    public void setHumidity(Double humidity) { this.humidity = formatToTwoDecimals(humidity); }
    public void setWindSpeed(Double windSpeed) { this.windSpeed = formatToTwoDecimals(windSpeed); }
    public void setAirQuality(Double airQuality) { this.airQuality = formatToTwoDecimals(airQuality); }
    public void setSignalStrength(Double signalStrength) { this.signalStrength = formatToTwoDecimals(signalStrength); }
    public void setCpuUtilization(Double cpuUtilization) { this.cpuUtilization = formatToTwoDecimals(cpuUtilization); }
    public void setMemoryUsage(Double memoryUsage) { this.memoryUsage = formatToTwoDecimals(memoryUsage); }
    public void setVoltage(Double voltage) { this.voltage = formatToTwoDecimals(voltage); }
    public void setResponseTime(Double responseTime) { this.responseTime = formatToTwoDecimals(responseTime); }
    public void setThroughput(Double throughput) { this.throughput = formatToTwoDecimals(throughput); }
    public void setDiskSpace(Double diskSpace) { this.diskSpace = formatToTwoDecimals(diskSpace); }
    public void setErrorRate(Double errorRate) { this.errorRate = formatToTwoDecimals(errorRate); }
    public void setInterference(Double interference) { this.interference = formatToTwoDecimals(interference); }
    public void setPacketLoss(Double packetLoss) { this.packetLoss = formatToTwoDecimals(packetLoss); }
    public void setLatency(Double latency) { this.latency = formatToTwoDecimals(latency); }
    public void setJitter(Double jitter) { this.jitter = formatToTwoDecimals(jitter); }
    public void setBandwidth(Double bandwidth) { this.bandwidth = formatToTwoDecimals(bandwidth); }
    public void setVibration(Double vibration) { this.vibration = formatToTwoDecimals(vibration); }
    public void setWindDirection(String windDirection) { this.windDirection = windDirection; }
    public void setUvIndex(Double uvIndex) { this.uvIndex = formatToTwoDecimals(uvIndex); }
    public void setPrecipitation(Double precipitation) { this.precipitation = formatToTwoDecimals(precipitation); }
    public void setPressure(Double pressure) { this.pressure = formatToTwoDecimals(pressure); }
}
