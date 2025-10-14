#!/bin/bash

echo "🚀 Starting 5Sky Project - Complete Setup"
echo "=========================================="
echo ""

# Function to check if a service is running
check_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $name to start..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $name is running at $url"
            return 0
        fi
        echo "   Attempt $attempt/$max_attempts - waiting..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $name failed to start after $max_attempts attempts"
    return 1
}

# Start Docker services first
echo "🐳 Starting Docker services (Grafana + Prometheus)..."
cd /Users/mac/Desktop/PFE/Project
docker compose -f docker-compose.observability.yml up -d

# Wait a moment for Docker to start
sleep 5

# Start Backend
echo ""
echo "🔧 Starting Backend (Spring Boot)..."
cd /Users/mac/Desktop/PFE/Project/5skye-backend-main
nohup ./mvnw spring-boot:run > ../backend.log 2>&1 &
BACKEND_PID=$!

# Start Simulator
echo "🎮 Starting Simulator..."
cd /Users/mac/Desktop/PFE/Project/tower-telemetry-simulator
nohup ./mvnw spring-boot:run > ../simulator.log 2>&1 &
SIMULATOR_PID=$!

# Start Frontend
echo "🌐 Starting Frontend (Next.js)..."
cd /Users/mac/Desktop/PFE/Project/5skye-Frontend-main
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo ""
echo "⏳ Waiting for all services to start..."
echo "This may take 1-2 minutes..."
echo ""

# Check services
check_service "http://localhost:8088/api/towers" "Backend API"
check_service "http://localhost:8080/api/telemetry/live" "Simulator"
check_service "http://localhost:3000" "Frontend"
check_service "http://localhost:3001/api/health" "Grafana"

echo ""
echo "🎉 All services started successfully!"
echo ""
echo "📊 ACCESS YOUR APPLICATIONS:"
echo "• Frontend: http://localhost:3000"
echo "• Backend API: http://localhost:8088/api/towers"
echo "• Simulator: http://localhost:8080/api/telemetry/live"
echo "• Grafana: http://localhost:3001 (admin/admin)"
echo "• Prometheus: http://localhost:9090"
echo ""
echo "📋 PROCESS IDS (for stopping later):"
echo "• Backend PID: $BACKEND_PID"
echo "• Simulator PID: $SIMULATOR_PID"
echo "• Frontend PID: $FRONTEND_PID"
echo ""
echo "💡 To stop all services: ./stop-project.sh"
echo "📝 Logs are saved in: backend.log, simulator.log, frontend.log"






