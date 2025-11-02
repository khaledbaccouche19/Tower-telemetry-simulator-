#!/usr/bin/env python3
"""
Custom JSON Metrics Exporter for SiteBoss Data
This script fetches JSON data and exposes it as Prometheus metrics
"""

import json
import requests
import time
from prometheus_client import start_http_server, Gauge, Counter, Info
from typing import Dict, Any

class SiteBossMetricsExporter:
    def __init__(self, siteboss_url: str, port: int = 8000):
        self.siteboss_url = siteboss_url
        self.port = port
        
        # Define Prometheus metrics
        self.alert_count = Gauge('siteboss_alert_count_custom', 
                                'SiteBoss alert count by level', 
                                ['tower_id', 'level'])
        
        self.sensor_status = Gauge('siteboss_sensor_status_custom',
                                 'SiteBoss sensor status (0=normal, 1=warning, 2=critical)',
                                 ['tower_id', 'sensor_name', 'sensor_id', 'sensor_type'])
        
        self.temperature = Gauge('siteboss_temperature_custom',
                               'SiteBoss temperature readings',
                               ['tower_id', 'sensor_name', 'location'])
        
        self.sensor_type_count = Gauge('siteboss_sensor_type_count_custom',
                                     'SiteBoss sensor count by type',
                                     ['tower_id', 'sensor_type'])
        
        self.unit_info = Info('siteboss_unit_info_custom',
                            'SiteBoss unit information')
        
        self.pull_errors = Counter('siteboss_pull_errors_custom',
                                 'SiteBoss pull errors',
                                 ['tower_id'])
        
        self.last_pull = Gauge('siteboss_last_pull_timestamp_custom',
                             'Timestamp of last successful pull',
                             ['tower_id'])

    def fetch_siteboss_data(self) -> Dict[str, Any]:
        """Fetch JSON data from SiteBoss API"""
        try:
            response = requests.get(self.siteboss_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching SiteBoss data: {e}")
            return None

    def parse_uptime(self, uptime_str: str) -> float:
        """Parse uptime string to hours"""
        try:
            # Format: "764:04:36:23" (days:hours:minutes:seconds)
            parts = uptime_str.split(':')
            if len(parts) >= 4:
                days = int(parts[0])
                hours = int(parts[1])
                minutes = int(parts[2])
                seconds = int(parts[3])
                return days * 24 + hours + minutes/60 + seconds/3600
        except (ValueError, IndexError):
            pass
        return 0

    def parse_temperature(self, value_str: str) -> float:
        """Extract numeric temperature value"""
        try:
            # Remove non-numeric characters except decimal point and minus
            import re
            numeric_part = re.sub(r'[^\d.-]', '', value_str)
            return float(numeric_part)
        except (ValueError, TypeError):
            return 0

    def update_metrics(self, data: Dict[str, Any]):
        """Update Prometheus metrics from JSON data"""
        if not data:
            return

        tower_id = "49"  # Extract from data if available
        
        try:
            # Update alert counts
            if 'data' in data and 'summary' in data['data']:
                alert_counts = data['data']['summary'].get('alertCounts', {})
                for level, count in alert_counts.items():
                    self.alert_count.labels(tower_id=tower_id, level=level).set(count)
            
            # Update sensor status
            if 'data' in data and 'sensors' in data['data']:
                for sensor in data['data']['sensors']:
                    sensor_name = sensor.get('name', 'unknown')
                    sensor_id = sensor.get('id', 'unknown')
                    sensor_type = sensor.get('type', 'unknown')
                    alert_level = sensor.get('alertLevel', 'normal')
                    
                    # Convert alert level to numeric value
                    status_value = 0  # normal
                    if alert_level == 'warning':
                        status_value = 1
                    elif alert_level == 'critical':
                        status_value = 2
                    
                    self.sensor_status.labels(
                        tower_id=tower_id,
                        sensor_name=sensor_name,
                        sensor_id=sensor_id,
                        sensor_type=sensor_type
                    ).set(status_value)
                    
                    # Extract temperature values
                    if sensor_type == 'Temperature':
                        temp_value = self.parse_temperature(sensor.get('value', '0'))
                        self.temperature.labels(
                            tower_id=tower_id,
                            sensor_name=sensor_name,
                            location=sensor.get('group', 'unknown')
                        ).set(temp_value)
            
            # Update sensor type counts
            if 'data' in data and 'summary' in data['data']:
                sensor_types = data['data']['summary'].get('sensorsByType', {})
                for sensor_type, count in sensor_types.items():
                    self.sensor_type_count.labels(
                        tower_id=tower_id,
                        sensor_type=sensor_type
                    ).set(count)
            
            # Update unit info
            if 'data' in data and 'unit' in data['data']:
                unit = data['data']['unit']
                self.unit_info.labels(
                    site_name=unit.get('siteName', 'unknown'),
                    serial=unit.get('serial', 'unknown'),
                    version=unit.get('version', 'unknown'),
                    hardware=unit.get('hardware', 'unknown')
                ).set(1)  # Info metrics need a value
            
            # Update last pull timestamp
            self.last_pull.labels(tower_id=tower_id).set(time.time())
            
        except Exception as e:
            print(f"Error updating metrics: {e}")
            self.pull_errors.labels(tower_id=tower_id).inc()

    def run(self):
        """Main loop"""
        print(f"Starting SiteBoss metrics exporter on port {self.port}")
        start_http_server(self.port)
        
        while True:
            try:
                data = self.fetch_siteboss_data()
                self.update_metrics(data)
                print(f"Metrics updated at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            except KeyboardInterrupt:
                print("Exiting...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
            
            time.sleep(30)  # Update every 30 seconds

if __name__ == '__main__':
    exporter = SiteBossMetricsExporter(
        siteboss_url='http://localhost:8088/api/siteboss/latest',
        port=8000
    )
    exporter.run()












