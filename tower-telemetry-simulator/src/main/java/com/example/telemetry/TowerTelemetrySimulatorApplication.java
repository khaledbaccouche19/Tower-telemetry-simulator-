package com.example.telemetry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class TowerTelemetrySimulatorApplication {
    public static void main(String[] args) {
        SpringApplication.run(TowerTelemetrySimulatorApplication.class, args);
    }
}
