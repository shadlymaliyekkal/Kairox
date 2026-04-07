#!/usr/bin/env bash

set -euo pipefail

echo "[+] KAIROX Installer Started"

# -------------------------------

# Update system

# -------------------------------

echo "[+] Updating system..."
sudo apt update -y

# -------------------------------

# Install base dependencies

# -------------------------------

echo "[+] Installing required packages..."
sudo apt install -y git curl wget python3 python3-pip python3-venv nmap

# -------------------------------

# Setup Python virtual environment

# -------------------------------

echo "[+] Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
python3 -m venv venv
fi

source venv/bin/activate

echo "[+] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# -------------------------------

# Install Go if not installed

# -------------------------------

echo "[+] Checking Go installation..."

if ! command -v go >/dev/null 2>&1; then
echo "[+] Installing Go..."
wget -q https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
export PATH=$PATH:/usr/local/go/bin
else
echo "[+] Go already installed"
fi

export PATH="$PATH:$(go env GOPATH)/bin"

# -------------------------------

# Install recon tools

# -------------------------------

echo "[+] Installing recon tools..."

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/owasp-amass/amass/v4/...@master

# -------------------------------

# Verify installation

# -------------------------------

echo "[+] Verifying installation..."

for tool in subfinder amass httpx gau nmap; do
if command -v "$tool" >/dev/null 2>&1; then
echo "[+] $tool OK"
else
echo "[!] $tool missing"
fi
done

echo ""
echo "[+] Setup Completed Successfully"
echo ""
echo "Run KAIROX with:"
echo "source venv/bin/activate"
echo "python kairox.py"
