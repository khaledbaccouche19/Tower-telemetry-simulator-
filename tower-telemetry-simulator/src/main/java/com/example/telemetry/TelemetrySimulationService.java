package com.example.telemetry;

import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Service
public class TelemetrySimulationService {
    
    private Random random = new Random();
    
    // Environmental base values that change slowly over time
    private double baseTemperature = 25.0; // More realistic base temperature
    private double baseHumidity = 55.0;    // More realistic base humidity
    private double baseWindSpeed = 12.0;   // More realistic base wind speed
    private double basePressure = 1013.0;  // Atmospheric pressure baseline
    
    // System health metrics with realistic aging
    private double baseBattery = 100.0;    // Start with full battery
    private double baseUptime = 99.98;     // Very high uptime for telecom towers
    private double equipmentAge = 0.0;     // Equipment aging factor (0-1)
    
    // Time-based patterns
    private long simulationStartTime = System.currentTimeMillis();
    private double dailyCycle = 0.0;       // 0-1 representing daily cycle
    private double weeklyCycle = 0.0;      // 0-1 representing weekly cycle
    
    public List<TelemetryData> generateLiveData() {
        List<TelemetryData> data = new ArrayList<>();
        
        // Generate generic telemetry data (no tower association)
        data.add(generateSimplifiedTowerData());
        
        return data;
    }
    
    private TelemetryData generateSimplifiedTowerData() {
        TelemetryData data = new TelemetryData();
        
        // Generate generic telemetry data (no tower association)
        data.setTowerId(null);
        data.setTowerName(null);
        data.setStatus("online");
        
        // Update base values slowly (realistic tower behavior)
        updateBaseValues();
        
        // Get current time for realistic patterns
        int hour = LocalDateTime.now().getHour();
        int dayOfWeek = LocalDateTime.now().getDayOfWeek().getValue();
        
        // ENVIRONMENTAL METRICS - Very realistic with minimal variation
        double ambientTemp = baseTemperature + (random.nextGaussian() * 0.1); // Tiny variation
        data.setAmbientTemperature(Math.max(15.0, Math.min(45.0, ambientTemp)));
        
        // Tower temperature correlates with ambient + equipment heat + time of day
        double equipmentHeat = 8.0 + (random.nextGaussian() * 0.05); // Very small variation
        double timeOfDayEffect = Math.sin((hour - 6) * Math.PI / 12) * 0.5; // Smaller daily cycle
        double towerTemp = ambientTemp + equipmentHeat + timeOfDayEffect + (random.nextGaussian() * 0.05);
        data.setTemperature(Math.max(25.0, Math.min(55.0, towerTemp)));
        
        // Humidity inversely correlates with temperature and has daily patterns
        double humidityBase = baseHumidity - (ambientTemp - 25.0) * 0.2; // Smaller correlation
        double humidityVariation = random.nextGaussian() * 0.2; // Tiny variation
        data.setHumidity(Math.max(30.0, Math.min(85.0, humidityBase + humidityVariation)));
        
        // Wind affects multiple parameters
        double windSpeed = baseWindSpeed + (random.nextGaussian() * 0.2); // Tiny variation
        data.setWindSpeed(Math.max(2.0, Math.min(35.0, windSpeed)));
        data.setWindDirection(getRealisticWindDirection(windSpeed));
        
        // Air quality correlates with humidity, wind, and time of day
        double airQualityBase = 75.0 - (data.getHumidity() - 50.0) * 0.1 + (windSpeed * 0.05); // Smaller correlations
        double rushHourEffect = (hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19) ? -1.0 : 0.0; // Smaller effect
        data.setAirQuality(Math.max(40.0, Math.min(95.0, airQualityBase + rushHourEffect + (random.nextGaussian() * 0.1))));
        
        // UV index follows realistic daily pattern
        double uvBase = getUVIndexForHour(hour);
        data.setUvIndex(Math.max(0.0, Math.min(12.0, uvBase + (random.nextGaussian() * 0.1))));
        
        // Pressure varies realistically
        double pressure = basePressure + (random.nextGaussian() * 0.5);
        data.setPressure(Math.max(1010.0, Math.min(1020.0, pressure)));
        
        // Precipitation correlates with humidity and pressure
        double precipitationChance = (data.getHumidity() > 75.0 && pressure < 1010.0) ? 0.4 : 0.05;
        double precipitation = random.nextDouble() < precipitationChance ? 
            random.nextDouble() * 2.5 : 0.0;
        data.setPrecipitation(precipitation);
        
        // Vibration correlates with wind speed
        double vibration = 0.02 + (random.nextGaussian() * 0.005);
        data.setVibration(Math.max(0.01, Math.min(0.03, vibration)));
        
        // SYSTEM HEALTH METRICS - More realistic aging and patterns
        // Battery always stays at 100%
        data.setBattery(100.0);
        
        // Uptime is very high but can have minor fluctuations
        double uptimeVariation = random.nextGaussian() * 0.01;
        data.setUptime(Math.max(99.7, Math.min(100.0, baseUptime + uptimeVariation)));
        
        // NETWORK METRICS - Extremely stable with minimal variation
        double baseNetworkLoad = 50.0;
        double rushHourMultiplier = (hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19) ? 1.02 : 1.0; // Tiny rush hour effect
        double weekendMultiplier = (dayOfWeek == 6 || dayOfWeek == 7) ? 0.98 : 1.0; // Tiny weekend effect
        double networkLoad = baseNetworkLoad * rushHourMultiplier * weekendMultiplier + (random.nextGaussian() * 0.1); // Minimal variation
        data.setNetworkLoad(Math.max(48.0, Math.min(52.0, networkLoad)));
        
        // Signal strength correlates with environmental conditions
        double signalBase = -65.0;
        double weatherEffect = (data.getHumidity() > 70.0) ? 0.1 : 0.0; // Minimal weather effect
        double windEffect = (windSpeed > 20.0) ? 0.05 : 0.0; // Minimal wind effect
        double signalStrength = signalBase + weatherEffect + windEffect + (random.nextGaussian() * 0.02); // Minimal variation
        data.setSignalStrength(Math.max(-66.0, Math.min(-64.0, signalStrength)));
        
        // Latency correlates with network load, signal strength, and environmental conditions
        double latencyBase = 18.0 + (networkLoad - 50.0) * 0.01; // Minimal correlations
        double weatherLatency = (data.getHumidity() > 70.0) ? 0.05 : 0.0; // Minimal weather effect
        double latency = latencyBase + weatherLatency + (random.nextGaussian() * 0.02); // Minimal variation
        data.setLatency(Math.max(17.8, Math.min(18.2, latency)));
        
        // Jitter correlates with latency and network conditions
        double jitter = 1.0 + (random.nextGaussian() * 0.01); // Minimal variation
        data.setJitter(Math.max(0.98, Math.min(1.02, jitter)));
        
        // Packet loss correlates with network load, signal strength, and environmental stress
        double packetLossBase = 0.01 + (random.nextGaussian() * 0.001); // Very stable
        data.setPacketLoss(Math.max(0.0, Math.min(0.02, packetLossBase)));
        
        // Bandwidth correlates with signal strength, network load, and environmental conditions
        double bandwidthBase = 600.0 + (random.nextGaussian() * 0.5); // Very stable
        data.setBandwidth(Math.max(598.0, Math.min(602.0, bandwidthBase)));
        
        // Throughput correlates with bandwidth and network load
        double throughput = data.getBandwidth() * 0.85 + (random.nextGaussian() * 0.5);
        data.setThroughput(Math.max(508.0, Math.min(512.0, throughput)));
        
        // Response time correlates with latency and network load
        double responseTime = 20.0 + (random.nextGaussian() * 0.1);
        data.setResponseTime(Math.max(19.8, Math.min(20.2, responseTime)));
        
        // CPU and memory correlate with network load and time patterns
        double cpuBase = 40.0 + (random.nextGaussian() * 0.2);
        data.setCpuUtilization(Math.max(39.5, Math.min(40.5, cpuBase)));
        
        double memoryBase = 60.0 + (random.nextGaussian() * 0.1);
        data.setMemoryUsage(Math.max(59.8, Math.min(60.2, memoryBase)));
        
        // Disk space decreases slowly over time (realistic)
        double diskSpace = 75.0 + (random.nextGaussian() * 0.1);
        data.setDiskSpace(Math.max(74.8, Math.min(75.2, diskSpace)));
        
        // Error rates correlate with environmental stress and system load
        double errorRateBase = 0.01 + (random.nextGaussian() * 0.001);
        data.setErrorRate(Math.max(0.0, Math.min(0.02, errorRateBase)));
        
        // Interference correlates with environmental conditions
        double interferenceBase = 5.0 + (random.nextGaussian() * 0.1);
        data.setInterference(Math.max(4.8, Math.min(5.2, interferenceBase)));
        
        // Voltage is very stable with minor variations
        double voltage = 12.5 + (random.nextGaussian() * 0.01);
        data.setVoltage(Math.max(12.4, Math.min(12.6, voltage)));
        
        // Fix timestamp formatting issue - use the exact format requested
        String timestamp = LocalDateTime.now().atZone(ZoneOffset.UTC).format(DateTimeFormatter.ISO_INSTANT);
        data.setTimestamp(timestamp);
        
        return data;
    }
    
    private TelemetryData generateRealisticTowerData(Long towerId, String towerName) {
        TelemetryData data = new TelemetryData();
        // Tower association will be handled by the calling system
        data.setTowerId(null);
        data.setTowerName(null);
        
        // Update base values slowly (realistic tower behavior)
        updateBaseValues();
        
        // Format current timestamp
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_INSTANT);
        data.setTimestamp(timestamp);
        
        // Generate correlated, realistic telemetry data
        
        // Environmental conditions (correlated)
        double ambientTemp = baseTemperature + (random.nextGaussian() * 3.0); // ±3°C variation
        data.setAmbientTemperature(Math.max(15.0, Math.min(45.0, ambientTemp)));
        
        // Tower temperature correlates with ambient + equipment heat
        double equipmentHeat = 8.0 + (random.nextGaussian() * 2.0); // Equipment generates heat
        double towerTemp = ambientTemp + equipmentHeat + (random.nextGaussian() * 1.5);
        data.setTemperature(Math.max(30.0, Math.min(55.0, towerTemp)));
        
        // Humidity inversely correlates with temperature
        double humidityVariation = random.nextGaussian() * 5.0;
        double humidity = baseHumidity - (ambientTemp - 25.0) * 0.8 + humidityVariation;
        data.setHumidity(Math.max(30.0, Math.min(85.0, humidity)));
        
        // Wind affects multiple parameters
        double windSpeed = baseWindSpeed + (random.nextGaussian() * 4.0);
        data.setWindSpeed(Math.max(2.0, Math.min(35.0, windSpeed)));
        
        // Wind direction based on wind speed (calm = random, windy = more consistent)
        data.setWindDirection(getRealisticWindDirection(windSpeed));
        
        // Air quality correlates with humidity and wind
        double airQualityBase = 85.0 - (humidity - 50.0) * 0.3 + (windSpeed * 0.2);
        double airQuality = airQualityBase + (random.nextGaussian() * 3.0);
        data.setAirQuality(Math.max(65.0, Math.min(98.0, airQuality)));
        
        // UV index correlates with time of day and weather
        int hour = LocalDateTime.now().getHour();
        double uvBase = getUVIndexForHour(hour);
        double uvVariation = random.nextGaussian() * 1.5;
        data.setUvIndex(Math.max(0.0, Math.min(12.0, uvBase + uvVariation)));
        
        // Precipitation correlates with humidity and air pressure
        double pressure = 1013.0 + (random.nextGaussian() * 8.0);
        data.setPressure(Math.max(990.0, Math.min(1040.0, pressure)));
        
        double precipitationChance = (humidity > 70.0 && pressure < 1010.0) ? 0.3 : 0.05;
        double precipitation = random.nextDouble() < precipitationChance ? 
            random.nextDouble() * 3.0 : 0.0;
        data.setPrecipitation(precipitation);
        
        // Vibration correlates with wind speed
        double vibration = (windSpeed > 20.0) ? 
            (windSpeed - 20.0) * 0.02 + random.nextDouble() * 0.1 : 
            random.nextDouble() * 0.05;
        data.setVibration(Math.min(0.8, vibration));
        
        // System health metrics (more stable, realistic)
        data.setBattery(100.0);
        data.setUptime(Math.max(99.8, Math.min(100.0, baseUptime + (random.nextGaussian() * 0.02))));
        
        // CPU and memory correlate with network load
        double networkLoad = 60.0 + (random.nextGaussian() * 15.0);
        data.setNetworkLoad(Math.max(40.0, Math.min(95.0, networkLoad)));
        
        double cpuBase = 40.0 + (networkLoad * 0.3);
        data.setCpuUtilization(Math.max(25.0, Math.min(85.0, cpuBase + (random.nextGaussian() * 5.0))));
        
        double memoryBase = 65.0 + (networkLoad * 0.2);
        data.setMemoryUsage(Math.max(55.0, Math.min(90.0, memoryBase + (random.nextGaussian() * 3.0))));
        
        // Disk space decreases slowly over time (realistic)
        double diskSpace = 85.0 - (random.nextDouble() * 20.0);
        data.setDiskSpace(Math.max(50.0, Math.min(90.0, diskSpace)));
        
        // Network performance correlates with environmental conditions
        double signalStrengthBase = -65.0;
        double signalVariation = (humidity > 70.0) ? 8.0 : 3.0; // Rain affects signal
        double signalStrength = signalStrengthBase + (random.nextGaussian() * signalVariation);
        data.setSignalStrength(Math.max(-75.0, Math.min(-45.0, signalStrength)));
        
        // Throughput correlates with signal strength and network load
        double throughputBase = 800.0 + (signalStrength + 70.0) * 10.0;
        double throughput = throughputBase + (random.nextGaussian() * 50.0);
        data.setThroughput(Math.max(400.0, Math.min(1000.0, throughput)));
        
        // Latency correlates with network load and environmental conditions
        double latencyBase = 20.0 + (networkLoad * 0.2) + (humidity > 70.0 ? 5.0 : 0.0);
        double latency = latencyBase + (random.nextGaussian() * 3.0);
        data.setLatency(Math.max(12.0, Math.min(45.0, latency)));
        
        // Jitter correlates with latency
        double jitter = latency * 0.15 + (random.nextGaussian() * 1.0);
        data.setJitter(Math.max(1.0, Math.min(12.0, jitter)));
        
        // Response time correlates with latency and CPU
        double responseTime = latency + (data.getCpuUtilization() * 0.1) + (random.nextGaussian() * 2.0);
        data.setResponseTime(Math.max(15.0, Math.min(55.0, responseTime)));
        
        // Bandwidth correlates with throughput
        double bandwidth = throughput * 0.8 + (random.nextGaussian() * 30.0);
        data.setBandwidth(Math.max(80.0, Math.min(950.0, bandwidth)));
        
        // Error rates correlate with environmental stress
        double errorRateBase = 0.02 + (humidity > 75.0 ? 0.03 : 0.0) + (towerTemp > 45.0 ? 0.02 : 0.0);
        double errorRate = errorRateBase + (random.nextGaussian() * 0.01);
        data.setErrorRate(Math.max(0.0, Math.min(0.08, errorRate)));
        
        // Packet loss correlates with error rate and network load
        double packetLossBase = errorRate * 2.0 + (networkLoad > 80.0 ? 0.05 : 0.0);
        double packetLoss = packetLossBase + (random.nextGaussian() * 0.02);
        data.setPacketLoss(Math.max(0.0, Math.min(0.15, packetLoss)));
        
        // Interference correlates with environmental conditions
        double interferenceBase = 8.0 + (humidity > 70.0 ? 5.0 : 0.0) + (windSpeed > 25.0 ? 3.0 : 0.0);
        double interference = interferenceBase + (random.nextGaussian() * 2.0);
        data.setInterference(Math.max(3.0, Math.min(28.0, interference)));
        
        // Voltage is very stable with minor variations
        double voltage = 12.5 + (random.nextGaussian() * 0.15);
        data.setVoltage(Math.max(11.8, Math.min(13.2, voltage)));
        
        return data;
    }
    
    private void updateBaseValues() {
        // Extremely slow drift with momentum (realistic tower behavior)
        baseTemperature += (random.nextGaussian() * 0.005); // Even smaller changes
        baseHumidity += (random.nextGaussian() * 0.008);
        baseWindSpeed += (random.nextGaussian() * 0.01);
        basePressure += (random.nextGaussian() * 0.02);
        
        // Battery always stays at 100% - no power outages, no variations
        baseBattery = 100.0;
        
        // Uptime stays very high (realistic for telecom towers) with occasional minor dips
        if (baseUptime < 99.95) {
            baseUptime += 0.000005; // Very slow recovery
        } else if (random.nextDouble() < 0.00005) { // 0.005% chance of minor uptime fluctuation
            baseUptime -= 0.00005; // Very small dip
        }
        
        // Equipment aging affects performance over time
        equipmentAge += 0.0000005; // Very slow aging
        
        // Keep values in realistic ranges
        baseTemperature = Math.max(18.0, Math.min(48.0, baseTemperature));
        baseHumidity = Math.max(30.0, Math.min(85.0, baseHumidity));
        baseWindSpeed = Math.max(3.0, Math.min(35.0, baseWindSpeed));
        basePressure = Math.max(985.0, Math.min(1045.0, basePressure));
        baseBattery = 100.0; // Always 100%
        baseUptime = Math.max(99.5, Math.min(100.0, baseUptime));
        equipmentAge = Math.min(1.0, equipmentAge);
    }
    
    private String getRealisticWindDirection(double windSpeed) {
        // Wind direction stays very stable - only changes rarely
        String[] directions = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"};
        
        // 95% chance to keep same direction, 5% chance to change
        if (random.nextDouble() < 0.95) {
            return "E"; // Default stable direction
        } else {
            return directions[random.nextInt(directions.length)];
        }
    }
    
    private double getUVIndexForHour(int hour) {
        // UV index follows realistic daily pattern with seasonal variation
        double baseUV;
        
        if (hour >= 6 && hour <= 18) {
            // Calculate UV based on sun angle (simplified)
            double sunAngle = Math.sin((hour - 6) * Math.PI / 12);
            baseUV = sunAngle * 10.0; // Peak at noon
            
            if (hour >= 10 && hour <= 14) {
                baseUV += 2.0; // Peak hours boost
            }
        } else {
            baseUV = 0.2; // Very low at night
        }
        
        // Add some realistic variation
        double variation = random.nextGaussian() * 1.2;
        return Math.max(0.0, Math.min(12.0, baseUV + variation));
    }
    
    // NEW METHODS for frontend integration
    
    public List<TelemetryData> generateHistoricalData(Long towerId, String timeRange) {
        List<TelemetryData> historicalData = new ArrayList<>();
        int dataPoints = getDataPointsForTimeRange(timeRange);
        
        for (int i = 0; i < dataPoints; i++) {
            TelemetryData data = generateRealisticTowerData(towerId, null);
            // Adjust timestamp to be in the past - fix the formatting issue
            data.setTimestamp(LocalDateTime.now().minusMinutes(i * 5).atZone(ZoneOffset.UTC).format(DateTimeFormatter.ISO_INSTANT));
            historicalData.add(data);
        }
        
        return historicalData;
    }
    
    public List<TowerSummary> generateTowerSummaries() {
        List<TowerSummary> summaries = new ArrayList<>();
        // Tower summaries will be generated by the calling system
        return summaries;
    }
    
    public List<Tower> getAllTowers() {
        List<Tower> towers = new ArrayList<>();
        // Tower list will be generated by the calling system
        return towers;
    }
    
    private TowerSummary createTowerSummary(Long id, String name, String status, Double battery, Double temperature, Double uptime, Double networkLoad, String city, String region, String useCase) {
        TowerSummary summary = new TowerSummary();
        summary.setId(id);
        summary.setName(name);
        summary.setStatus(status);
        summary.setBattery(battery);
        summary.setTemperature(temperature);
        summary.setUptime(uptime);
        summary.setNetworkLoad(networkLoad);
        summary.setCity(city);
        summary.setRegion(region);
        summary.setUseCase(useCase);
        summary.setLastMaintenance(LocalDateTime.now().minusDays(30));
        return summary;
    }
    
    private Tower createTower(Long id, String name, String status, Double latitude, Double longitude, String city, String useCase, String region) {
        Tower tower = new Tower();
        tower.setId(id);
        tower.setName(name);
        tower.setStatus(status);
        tower.setLatitude(latitude);
        tower.setLongitude(longitude);
        tower.setCity(city);
        tower.setUseCase(useCase);
        tower.setRegion(region);
        tower.setCreatedAt(LocalDateTime.now().minusDays(30));
        tower.setUpdatedAt(LocalDateTime.now());
        return tower;
    }
    
    private String getTowerName(Long towerId) {
        return null; // Tower names will be handled by the calling system
    }
    
    private int getDataPointsForTimeRange(String timeRange) {
        switch (timeRange) {
            case "1h": return 12;    // 5-minute intervals for 1 hour
            case "24h": return 288;  // 5-minute intervals for 24 hours
            case "7d": return 2016;  // 5-minute intervals for 7 days
            case "30d": return 8640; // 5-minute intervals for 30 days
            default: return 288;     // Default to 24 hours
        }
    }
}
