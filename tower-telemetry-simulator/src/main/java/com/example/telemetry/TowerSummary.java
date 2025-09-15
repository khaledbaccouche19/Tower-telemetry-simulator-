package com.example.telemetry;

import java.time.LocalDateTime;

public class TowerSummary {
    private Long id;
    private String name;
    private String status;
    private Double battery;
    private Double temperature;
    private Double uptime;
    private Double networkLoad;
    private String city;
    private String region;
    private String useCase;
    private LocalDateTime lastMaintenance;
    
    // Default constructor
    public TowerSummary() {}
    
    // Constructor with parameters
    public TowerSummary(Long id, String name, String status, Double battery, Double temperature, 
                       Double uptime, Double networkLoad, String city, String region, String useCase, 
                       LocalDateTime lastMaintenance) {
        this.id = id;
        this.name = name;
        this.status = status;
        this.battery = battery;
        this.temperature = temperature;
        this.uptime = uptime;
        this.networkLoad = networkLoad;
        this.city = city;
        this.region = region;
        this.useCase = useCase;
        this.lastMaintenance = lastMaintenance;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public Double getBattery() { return battery; }
    public void setBattery(Double battery) { this.battery = battery; }
    
    public Double getTemperature() { return temperature; }
    public void setTemperature(Double temperature) { this.temperature = temperature; }
    
    public Double getUptime() { return uptime; }
    public void setUptime(Double uptime) { this.uptime = uptime; }
    
    public Double getNetworkLoad() { return networkLoad; }
    public void setNetworkLoad(Double networkLoad) { this.networkLoad = networkLoad; }
    
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    
    public String getRegion() { return region; }
    public void setRegion(String region) { this.region = region; }
    
    public String getUseCase() { return useCase; }
    public void setUseCase(String useCase) { this.useCase = useCase; }
    
    public LocalDateTime getLastMaintenance() { return lastMaintenance; }
    public void setLastMaintenance(LocalDateTime lastMaintenance) { this.lastMaintenance = lastMaintenance; }
}
