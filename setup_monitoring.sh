#!/bin/bash

echo "📊 Setting up SiteBoss & Simulator Monitoring Dashboard"
echo "======================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Create directories
mkdir -p grafana/data
mkdir -p prometheus/data

# Start Prometheus
echo "🚀 Starting Prometheus..."
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus_siteboss.yml:/etc/prometheus/prometheus.yml \
  -v prometheus_data:/prometheus \
  prom/prometheus:latest

# Start Grafana
echo "🚀 Starting Grafana..."
docker run -d \
  --name grafana \
  -p 3001:3000 \
  -v grafana_data:/var/lib/grafana \
  -v $(pwd)/grafana/dashboards:/var/lib/grafana/dashboards \
  -v $(pwd)/grafana/provisioning:/etc/grafana/provisioning \
  grafana/grafana:latest

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status:"
echo "Prometheus: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:9090)"
echo "Grafana: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3001)"

echo ""
echo "🎉 Monitoring setup complete!"
echo ""
echo "📊 Access your dashboards:"
echo "  Grafana: http://localhost:3001 (admin/admin)"
echo "  Prometheus: http://localhost:9090"
echo ""
echo "📋 Next steps:"
echo "  1. Open Grafana at http://localhost:3001"
echo "  2. Login with admin/admin"
echo "  3. Add Prometheus data source: http://prometheus:9090"
echo "  4. Import the SiteBoss monitoring dashboard"
echo ""
echo "🔧 To stop services:"
echo "  docker stop prometheus grafana"
echo "  docker rm prometheus grafana"












