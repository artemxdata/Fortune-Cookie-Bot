#!/bin/bash

# Fortune Cookie Bot Deployment Script
# Run with: bash deploy.sh

echo "🍪 Starting Fortune Cookie Bot deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BOT_DIR="/root/Fortune-Cookie-Bot"
SERVICE_NAME="fortune-cookie-bot"
VENV_DIR="$BOT_DIR/venv"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Stop existing service if running
print_status "Stopping existing bot service..."
systemctl stop $SERVICE_NAME 2>/dev/null || true

# Update code from git
if [ -d "$BOT_DIR/.git" ]; then
    print_status "Updating code from git..."
    cd $BOT_DIR
    git pull origin main
else
    print_warning "Not a git repository. Skipping git pull."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_status "Creating virtual environment..."
    cd $BOT_DIR
    python3 -m venv venv
fi

# Activate virtual environment and install/update packages
print_status "Installing/updating Python packages..."
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p $BOT_DIR/data
mkdir -p $BOT_DIR/quotes/{memes_images,memes_loves,memes_work,memes_psy,memes_friendship,start_image,donate_picture}

# Set permissions
print_status "Setting permissions..."
chown -R root:root $BOT_DIR
chmod +x $BOT_DIR/main.py

# Check if .env file exists
if [ ! -f "$BOT_DIR/.env" ]; then
    print_warning ".env file not found!"
    print_warning "Please create .env file with BOT_TOKEN=your_token_here"
    print_warning "Template available in config_example.py"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
