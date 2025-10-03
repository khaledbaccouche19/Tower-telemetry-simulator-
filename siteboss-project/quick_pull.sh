#!/bin/bash
# SiteBoss Quick Pull Script
# Usage: ./quick_pull.sh [IP] [USER] [PASS] [OUTPUT_FILE]

# Default values
DEFAULT_IP="10.9.1.19"
DEFAULT_USER="admin"
DEFAULT_PASS="password"
DEFAULT_OUTPUT="siteboss_$(date +%Y%m%d_%H%M%S).json"

# Use provided values or defaults
IP=${1:-$DEFAULT_IP}
USER=${2:-$DEFAULT_USER}
PASS=${3:-$DEFAULT_PASS}
OUTPUT=${4:-$DEFAULT_OUTPUT}

echo "🚀 SiteBoss Quick Pull"
echo "   IP: $IP"
echo "   User: $USER"
echo "   Output: $OUTPUT"
echo ""

# Check if virtual environment exists
if [ ! -d "siteboss-venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv siteboss-venv"
    echo "   source siteboss-venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo "   playwright install --with-deps"
    exit 1
fi

# Activate virtual environment and run
source siteboss-venv/bin/activate

echo "🔌 Pulling data from SiteBoss device..."
python siteboss_api_debug.py \
    --host "$IP" \
    --user "$USER" \
    --pass "$PASS" \
    --output "$OUTPUT" \
    --save-xml

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Data pull completed successfully!"
    echo "   JSON: $OUTPUT"
    echo "   XML:  ${OUTPUT%.json}.xml"
    echo ""
    echo "📊 Quick summary:"
    python -c "
import json
try:
    with open('$OUTPUT', 'r') as f:
        data = json.load(f)
        print(f'   Site: {data[\"unit\"][\"siteName\"]}')
        print(f'   Sensors: {data[\"summary\"][\"totalSensors\"]}')
        print(f'   Alerts: {data[\"summary\"][\"alertCounts\"]}')
except Exception as e:
    print(f'   Error reading data: {e}')
"
else
    echo "❌ Data pull failed. Check the error messages above."
    exit 1
fi
