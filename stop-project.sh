#!/bin/bash

echo "🛑 Stopping 5Sky Project - Complete Shutdown"
echo "============================================="
echo ""

# Stop Docker services
echo "🐳 Stopping Docker services..."
cd /Users/mac/Desktop/PFE/Project
docker compose -f docker-compose.observability.yml down

# Kill processes by name (safer approach)
echo "🔧 Stopping Backend..."
pkill -f "spring-boot:run"

echo "🎮 Stopping Simulator..."
pkill -f "tower-telemetry-simulator"

echo "🌐 Stopping Frontend..."
pkill -f "next dev"

echo "🧹 Cleaning up logs..."
rm -f /Users/mac/Desktop/PFE/Project/backend.log
rm -f /Users/mac/Desktop/PFE/Project/simulator.log
rm -f /Users/mac/Desktop/PFE/Project/frontend.log

echo ""
echo "✅ All services stopped successfully!"
echo ""
echo "💡 To start again tomorrow: ./start-project.sh"






