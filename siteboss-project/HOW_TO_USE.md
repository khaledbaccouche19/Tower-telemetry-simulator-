# SiteBoss Project - How to Use Guide

## 🎯 Overview
The SiteBoss project provides automated data extraction from SiteBoss devices using browser automation. It pulls XML data, converts it to JSON format, and prepares it for backend API consumption.

## 🛠️ Environment Setup

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- macOS/Linux/Windows
- Network access to SiteBoss device

### 1. Create Virtual Environment
```bash
cd /path/to/siteboss-project
python3 -m venv siteboss-venv
```

### 2. Activate Virtual Environment
```bash
# macOS/Linux
source siteboss-venv/bin/activate

# Windows
siteboss-venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Browser Dependencies
```bash
# Install Playwright browsers (required for automation)
playwright install chromium
playwright install --with-deps
```

## 🚀 Usage Commands

### Basic Data Pull
```bash
python siteboss_api.py --host <SITEBOSS_IP> --user <USERNAME> --pass <PASSWORD>
```

### Advanced Data Pull with Options
```bash
python siteboss_api.py \
  --host 10.9.1.19 \
  --user admin \
  --pass password \
  --output my_siteboss_data.json \
  --save-xml
```

### Debug Mode (Recommended for troubleshooting)
```bash
python siteboss_api_debug.py \
  --host 10.9.1.19 \
  --user admin \
  --pass password \
  --output debug_data.json \
  --save-xml
```

## 📋 Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--host` | Yes | SiteBoss device IP address | `10.9.1.19` |
| `--user` | Yes | Login username | `admin` |
| `--pass` | Yes | Login password | `password` |
| `--output` | No | Output JSON filename | `siteboss_data.json` |
| `--save-xml` | No | Also save raw XML file | Flag only |

## 📊 Output Data Structure

### JSON Output Format
```json
{
  "unit": {
    "siteName": "5Sky Demo Site",
    "serial": "360050631",
    "version": "2.12.480",
    "location": {
      "latitude": 49.702006766332,
      "longitude": 14.0053179478874
    },
    "timestamp": {
      "date": "10/03/25",
      "time": "11:55:52",
      "lastUpdated": "2025-10-03T11:55:52.123456"
    }
  },
  "sensors": [
    {
      "id": "INTERNAL_Contact_Closure_Door_Open___Front_1",
      "group": "INTERNAL",
      "type": "Contact Closure",
      "name": "Door Open - Front",
      "status": "Active",
      "value": "Open",
      "alertLevel": "warning",
      "enabled": true
    }
  ],
  "summary": {
    "totalSensors": 9,
    "sensorsByType": {
      "Contact Closure": 6,
      "Temperature": 2,
      "Output": 1
    },
    "alertCounts": {
      "normal": 6,
      "warning": 2,
      "critical": 1
    }
  }
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Timeout
```bash
# Use debug version with increased timeouts
python siteboss_api_debug.py --host <IP> --user <USER> --pass <PASS>
```

#### 2. Browser Not Found
```bash
# Reinstall browser dependencies
playwright install --force
```

#### 3. Authentication Failed
- Verify credentials
- Check if device is accessible via browser
- Ensure device is not in maintenance mode

#### 4. XML Parsing Error
- Check if device returned HTML instead of XML
- Verify device is fully operational
- Try again after a few minutes

### Debug Steps
1. Test network connectivity: `ping <SITEBOSS_IP>`
2. Test HTTP access: `curl -v http://<SITEBOSS_IP>/UnitLogin.html`
3. Use debug version: `python siteboss_api_debug.py`
4. Check logs for detailed error messages

## 🔄 Integration with Backend

### 1. Data Flow
```
SiteBoss Device → Python Script → JSON File → Backend API → Frontend
```

### 2. Backend Integration
The generated JSON can be consumed by the backend API:
```bash
# Example: Send data to backend
curl -X POST http://localhost:8088/api/siteboss/data \
  -H "Content-Type: application/json" \
  -d @siteboss_data.json
```

### 3. Automated Scheduling
Set up cron job for regular data pulls:
```bash
# Add to crontab (every 5 minutes)
*/5 * * * * cd /path/to/siteboss-project && source siteboss-venv/bin/activate && python siteboss_api.py --host 10.9.1.19 --user admin --pass password --output live_data.json
```

## 📁 File Structure
```
siteboss-project/
├── siteboss_api.py          # Main script
├── siteboss_api_debug.py    # Debug version with extended timeouts
├── requirements.txt         # Python dependencies
├── siteboss-venv/          # Virtual environment
├── *.json                  # Generated JSON data files
├── *.xml                   # Raw XML data files
└── HOW_TO_USE.md          # This guide
```

## 🚨 Important Notes

### Security
- Store credentials securely (use environment variables)
- Consider using key-based authentication if available
- Regularly rotate passwords

### Performance
- Device response time varies (30-60 seconds typical)
- Use debug version for slow connections
- Consider data caching for frequent pulls

### Maintenance
- Keep Playwright browsers updated
- Monitor device availability
- Check logs for errors

## 📞 Support

### Logs Location
- Script output: Console
- Browser logs: Playwright internal
- Device logs: SiteBoss web interface

### Common Commands
```bash
# Check Python version
python --version

# Check Playwright installation
playwright --version

# List installed browsers
playwright install --list

# Test basic connectivity
curl -I http://<SITEBOSS_IP>

# View recent data
ls -la *.json | head -5
```

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
source siteboss-venv/bin/activate
pip install --upgrade playwright
playwright install --force
```

### Backup Data
```bash
# Backup all data files
tar -czf siteboss_backup_$(date +%Y%m%d).tar.gz *.json *.xml
```

---

**Last Updated**: October 3, 2025  
**Version**: 1.0  
**Tested With**: SiteBoss v2.12.480, Python 3.13, Playwright 1.55.0
