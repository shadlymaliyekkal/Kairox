#!/bin/bash

echo "[+] Installing dependencies..."

sudo apt update -y
sudo apt install -y git curl wget python3-pip nmap

# Install Go if missing
if ! command -v go &> /dev/null
then
    wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    export PATH=$PATH:/usr/local/go/bin
fi

export PATH=$PATH:$(go env GOPATH)/bin

echo "[+] Installing recon tools..."
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/owasp-amass/amass/v4/...@master

echo "[+] Installing Python packages..."
pip install -r requirements.txt

echo "[+] Setup completed."