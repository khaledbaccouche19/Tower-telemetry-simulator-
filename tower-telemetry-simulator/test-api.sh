#!/bin/bash

echo "🚀 Testing Tower Telemetry Simulator API"
echo "========================================"

# Wait for application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Test health endpoint
echo "🏥 Testing health endpoint..."
curl -s http://localhost:8080/api/telemetry/health
echo -e "\n"

# Test live telemetry endpoint
echo "📡 Testing live telemetry endpoint..."
curl -s http://localhost:8080/api/telemetry/live | python3 -m json.tool
echo -e "\n"

# Test tower summaries endpoint
echo "📊 Testing tower summaries endpoint..."
curl -s http://localhost:8080/api/towers/summaries | python3 -m json.tool
echo -e "\n"

# Test all towers endpoint
echo "🗼 Testing all towers endpoint..."
curl -s http://localhost:8080/api/towers | python3 -m json.tool
echo -e "\n"

# Test historical data endpoint
echo "📈 Testing historical data endpoint (24h)..."
curl -s "http://localhost:8080/api/telemetry/tower/1/history?timeRange=24h" | python3 -m json.tool | head -50
echo -e "\n"

echo "✅ API testing completed!"
