package com.example.telemetry;

import java.time.LocalDateTime;

public class Tower {
    private Long id;
    private String name;
    private String status;
    private Double latitude;
    private Double longitude;
    private String city;
    private String useCase;
    private String region;
    private String model3dPath;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // Default constructor
    public Tower() {}
    
    // Constructor with parameters
    public Tower(Long id, String name, String status, Double latitude, Double longitude, 
                String city, String useCase, String region, String model3dPath, 
                LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.id = id;
        this.name = name;
        this.status = status;
        this.latitude = latitude;
        this.longitude = longitude;
        this.city = city;
        this.useCase = useCase;
        this.region = region;
        this.model3dPath = model3dPath;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public Double getLatitude() { return latitude; }
    public void setLatitude(Double latitude) { this.latitude = latitude; }
    
    public Double getLongitude() { return longitude; }
    public void setLongitude(Double longitude) { this.longitude = longitude; }
    
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    
    public String getUseCase() { return useCase; }
    public void setUseCase(String useCase) { this.useCase = useCase; }
    
    public String getRegion() { return region; }
    public void setRegion(String region) { this.region = region; }
    
    public String getModel3dPath() { return model3dPath; }
    public void setModel3dPath(String model3dPath) { this.model3dPath = model3dPath; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
