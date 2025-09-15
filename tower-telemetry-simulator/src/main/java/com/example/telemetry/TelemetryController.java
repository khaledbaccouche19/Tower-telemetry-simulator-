package com.example.telemetry;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:3001"})
public class TelemetryController {
    
    @Autowired
    private TelemetrySimulationService telemetryService;
    
    @Autowired
    private DataRetentionService dataRetentionService;
    
    // Existing endpoint
    @GetMapping("/telemetry/live")
    public List<TelemetryData> getLiveTelemetry() {
        return telemetryService.generateLiveData();
    }
    
    // NEW ENDPOINTS for frontend integration
    
    @GetMapping("/telemetry/tower/{towerId}/history")
    public List<TelemetryData> getTelemetryHistory(
        @PathVariable Long towerId,
        @RequestParam(defaultValue = "24h") String timeRange
    ) {
        return telemetryService.generateHistoricalData(towerId, timeRange);
    }
    
    @GetMapping("/towers/summaries")
    public List<TowerSummary> getTowerSummaries() {
        return telemetryService.generateTowerSummaries();
    }
    
    @GetMapping("/towers")
    public List<Tower> getAllTowers() {
        return telemetryService.getAllTowers();
    }
    
    // NEW STORAGE MANAGEMENT ENDPOINTS
    
    @PostMapping("/telemetry/store")
    public String storeLiveData() {
        dataRetentionService.storeLiveData();
        return "Live telemetry data stored successfully";
    }
    
    @GetMapping("/storage/stats")
    public String getStorageStats() {
        return dataRetentionService.getStorageStats();
    }
    
    @GetMapping("/storage/count")
    public long getDataCount() {
        return dataRetentionService.getDataCount();
    }
    

}
