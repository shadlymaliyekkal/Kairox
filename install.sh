#!/usr/bin/env bash

# Auto-fix line endings (self-heal if CRLF)

sed -i 's/\r$//' "$0" 2>/dev/null || true

set -e

echo "[+] Starting KAIROX setup..."

# -------------------------------

# Update system

# -------------------------------

sudo apt update -y

# -------------------------------

# Install base packages

# -------------------------------

echo "[+] Installing dependencies..."
sudo apt install -y git curl wget python3-pip python3-venv nmap

# -------------------------------

# Setup virtual environment

# -------------------------------

echo "[+] Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
python3 -m venv venv
fi

source venv/bin/activate

# -------------------------------

# Install Python dependencies

# -------------------------------

echo "[+] Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# -------------------------------

# Install Go (if missing)

# -------------------------------

echo "[+] Checking Go installation..."

if ! command -v go &> /dev/null
then
echo "[+] Installing Go..."
wget -q https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
export PATH=$PATH:/usr/local/go/bin
else
echo "[+] Go already installed"
fi

export PATH=$PATH:$(go env GOPATH)/bin

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

echo "[+] Verifying tools..."

TOOLS=("subfinder" "amass" "httpx" "gau" "nmap")

for tool in "${TOOLS[@]}"
do
if command -v $tool &> /dev/null
then
echo "[+] $tool ready"
else
echo "[!] $tool missing"
fi
done

echo ""
echo "[+] Setup completed successfully"
echo ""
echo "To run KAIROX:"
echo "source venv/bin/activate"
echo "python kairox.py"
