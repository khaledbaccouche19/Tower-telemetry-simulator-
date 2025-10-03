# SiteBoss Data Integration Project

## 🎯 Purpose
Automated data extraction from SiteBoss devices for integration with the 5Sky Digital Twin Platform. This project provides browser automation to pull sensor data, convert it to JSON format, and prepare it for backend API consumption.

## 🚀 Quick Start

### 1. Setup Environment
```bash
./setup.sh
```

### 2. Pull Data
```bash
./quick_pull.sh [IP] [USER] [PASS]
```

### 3. Manual Usage
```bash
source siteboss-venv/bin/activate
python siteboss_api_debug.py --host 10.9.1.19 --user admin --pass password
```

## 📁 Project Structure
```
siteboss-project/
├── siteboss_api.py          # Main data pulling script
├── siteboss_api_debug.py    # Debug version with extended timeouts
├── quick_pull.sh            # Quick pull script
├── setup.sh                 # Environment setup script
├── requirements.txt         # Python dependencies
├── HOW_TO_USE.md           # Detailed usage guide
├── README.md               # This file
├── siteboss-venv/          # Python virtual environment
└── *.json, *.xml          # Generated data files
```

## 🔧 Features
- **Browser Automation**: Uses Playwright for reliable device interaction
- **Data Conversion**: Converts XML to structured JSON format
- **Error Handling**: Robust error handling and debugging
- **Flexible Output**: Configurable output formats and filenames
- **Integration Ready**: JSON format compatible with backend APIs

## 📊 Data Format
The script extracts:
- **Unit Information**: Site name, serial, version, location
- **Sensor Data**: Status, values, alert levels, types
- **Summary Statistics**: Total sensors, alert counts, sensor types

## 🛠️ Requirements
- Python 3.8+
- Playwright browsers (Chromium)
- Network access to SiteBoss device
- Valid device credentials

## 📚 Documentation
- **HOW_TO_USE.md**: Complete usage guide with examples
- **setup.sh**: Automated environment setup
- **quick_pull.sh**: One-command data pulling

## 🔄 Integration
This project integrates with:
- **5Sky Backend**: Spring Boot API on port 8088
- **5Sky Frontend**: Next.js dashboard on port 3000
- **Tower Simulator**: Telemetry simulator on port 8080

## 🚨 Troubleshooting
1. **Connection Issues**: Use debug version with extended timeouts
2. **Browser Errors**: Reinstall Playwright browsers
3. **Authentication**: Verify device credentials and accessibility

## 📞 Support
For issues or questions:
1. Check HOW_TO_USE.md for detailed troubleshooting
2. Use debug version for detailed error messages
3. Verify network connectivity and device status

---
**Version**: 1.0  
**Last Updated**: October 3, 2025  
**Compatible With**: SiteBoss v2.12.480+