package com.example.telemetry;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import jakarta.persistence.EntityManager;
import jakarta.persistence.Query;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
public class DataRetentionService {
    
    @Autowired
    private EntityManager entityManager;
    
    @Autowired
    private TelemetrySimulationService telemetryService;
    
    /**
     * Store live telemetry data in the database
     */
    @Transactional
    public void storeLiveData() {
        List<TelemetryData> liveData = telemetryService.generateLiveData();
        for (TelemetryData data : liveData) {
            entityManager.persist(data);
        }
        entityManager.flush();
    }
    
    /**
     * Clean up old data based on retention policy
     * Keep: 7 days of detailed data, 30 days of hourly summaries
     */
    @Scheduled(cron = "0 0 2 * * ?") // Run daily at 2 AM
    @Transactional
    public void cleanupOldData() {
        // Delete data older than 7 days
        LocalDateTime cutoffDate = LocalDateTime.now().minusDays(7);
        String cutoffTimestamp = cutoffDate.format(DateTimeFormatter.ISO_INSTANT);
        
        Query deleteQuery = entityManager.createQuery(
            "DELETE FROM TelemetryData t WHERE t.timestamp < :cutoff"
        );
        deleteQuery.setParameter("cutoff", cutoffTimestamp);
        
        int deletedCount = deleteQuery.executeUpdate();
        System.out.println("Cleaned up " + deletedCount + " old telemetry records");
    }
    
    /**
     * Get data count for monitoring
     */
    public long getDataCount() {
        Query countQuery = entityManager.createQuery("SELECT COUNT(t) FROM TelemetryData t");
        return (Long) countQuery.getSingleResult();
    }
    
    /**
     * Get storage statistics
     */
    public String getStorageStats() {
        long totalRecords = getDataCount();
        long recordsLast24h = getRecordsInLast24Hours();
        long recordsLast7d = getRecordsInLast7Days();
        
        return String.format(
            "Storage Stats: Total=%d, Last24h=%d, Last7d=%d",
            totalRecords, recordsLast24h, recordsLast7d
        );
    }
    
    private long getRecordsInLast24Hours() {
        LocalDateTime cutoffDate = LocalDateTime.now().minusHours(24);
        String cutoffTimestamp = cutoffDate.format(DateTimeFormatter.ISO_INSTANT);
        
        Query query = entityManager.createQuery(
            "SELECT COUNT(t) FROM TelemetryData t WHERE t.timestamp >= :cutoff"
        );
        query.setParameter("cutoff", cutoffTimestamp);
        
        return (Long) query.getSingleResult();
    }
    
    private long getRecordsInLast7Days() {
        LocalDateTime cutoffDate = LocalDateTime.now().minusDays(7);
        String cutoffTimestamp = cutoffDate.format(DateTimeFormatter.ISO_INSTANT);
        
        Query query = entityManager.createQuery(
            "SELECT COUNT(t) FROM TelemetryData t WHERE t.timestamp >= :cutoff"
        );
        query.setParameter("cutoff", cutoffTimestamp);
        
        return (Long) query.getSingleResult();
    }
}
