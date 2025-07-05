#!/bin/bash

# Install Twitter Auto Poster as a systemd service

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Installing Twitter Auto Poster as a systemd service${NC}"
echo "=================================================="

# Get current user and working directory
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Please don't run this script as root${NC}"
    exit 1
fi

# Check if service file exists
if [ ! -f "twitter-poster.service" ]; then
    echo -e "${RED}❌ Service file not found: twitter-poster.service${NC}"
    exit 1
fi

# Create a temporary service file with correct paths
TEMP_SERVICE=$(mktemp)
sed -e "s|your_username|$CURRENT_USER|g" \
    -e "s|/path/to/your/twitter-auto-poster|$CURRENT_DIR|g" \
    twitter-poster.service > "$TEMP_SERVICE"

echo -e "${YELLOW}📋 Service configuration:${NC}"
echo "User: $CURRENT_USER"
echo "Working Directory: $CURRENT_DIR"
echo "Python: $(which python3)"
echo ""

# Install service
echo -e "${GREEN}📦 Installing systemd service...${NC}"
sudo cp "$TEMP_SERVICE" /etc/systemd/system/twitter-poster.service

# Clean up
rm "$TEMP_SERVICE"

# Reload systemd
echo -e "${GREEN}🔄 Reloading systemd...${NC}"
sudo systemctl daemon-reload

# Enable service
echo -e "${GREEN}⚡ Enabling service...${NC}"
sudo systemctl enable twitter-poster.service

echo -e "${GREEN}✅ Service installed successfully!${NC}"
echo ""
echo "📋 Service management commands:"
echo "  Start:   sudo systemctl start twitter-poster"
echo "  Stop:    sudo systemctl stop twitter-poster"
echo "  Status:  sudo systemctl status twitter-poster"
echo "  Logs:    sudo journalctl -u twitter-poster -f"
echo "  Restart: sudo systemctl restart twitter-poster"
echo ""
echo -e "${YELLOW}⚠️  Make sure to configure your .env file before starting the service${NC}"
echo ""

read -p "Do you want to start the service now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}🚀 Starting service...${NC}"
    sudo systemctl start twitter-poster
    echo -e "${GREEN}✅ Service started${NC}"
    echo ""
    echo "Check status with: sudo systemctl status twitter-poster"
else
    echo -e "${YELLOW}⏭️  Service not started. Start it manually when ready.${NC}"
fi