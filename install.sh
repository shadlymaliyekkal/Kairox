#!/usr/bin/env bash
set -euo pipefail

# -------------------------------
# KAIROX Installer
# -------------------------------

echo "[+] KAIROX Installer Started"

# Detect script directory so relative paths work regardless of where you call it from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
VENV_DIR="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# FIX: Use venv's pip directly instead of relying on 'source activate' in a subshell
VENV_PIP="$VENV_DIR/bin/pip"
VENV_PYTHON="$VENV_DIR/bin/python"

echo "[+] Installing Python dependencies..."
"$VENV_PIP" install --upgrade pip

if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "[!] requirements.txt not found in $SCRIPT_DIR — skipping Python deps"
else
    "$VENV_PIP" install -r "$SCRIPT_DIR/requirements.txt"
fi

# -------------------------------
# Install Go if not installed
# -------------------------------
echo "[+] Checking Go installation..."

if ! command -v go >/dev/null 2>&1; then
    echo "[+] Installing Go..."

    # FIX: Detect OS architecture dynamically instead of hardcoding amd64
    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64)  GO_ARCH="amd64" ;;
        aarch64) GO_ARCH="arm64" ;;
        armv6l)  GO_ARCH="armv6l" ;;
        *)
            echo "[!] Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac

    # FIX: Fetch the latest stable Go version dynamically
    GO_VERSION=$(curl -fsSL "https://go.dev/VERSION?m=text" | head -1)
    GO_TARBALL="${GO_VERSION}.linux-${GO_ARCH}.tar.gz"
    GO_URL="https://go.dev/dl/${GO_TARBALL}"

    echo "[+] Downloading ${GO_TARBALL}..."
    wget -q "$GO_URL" -O "/tmp/${GO_TARBALL}"
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf "/tmp/${GO_TARBALL}"
    rm -f "/tmp/${GO_TARBALL}"

    # FIX: Write to ~/.profile as well for login shells; source immediately
    GO_EXPORT='export PATH=$PATH:/usr/local/go/bin'
    grep -qxF "$GO_EXPORT" ~/.bashrc || echo "$GO_EXPORT" >> ~/.bashrc
    grep -qxF "$GO_EXPORT" ~/.profile || echo "$GO_EXPORT" >> ~/.profile

    export PATH="$PATH:/usr/local/go/bin"
    echo "[+] Go installed: $(go version)"
else
    echo "[+] Go already installed: $(go version)"
fi

# FIX: Always ensure GOPATH/bin is in PATH for this session
export PATH="$PATH:$(go env GOPATH)/bin"

# Also persist GOPATH/bin for future sessions
GOPATH_EXPORT='export PATH=$PATH:$(go env GOPATH)/bin'
grep -qxF "$GOPATH_EXPORT" ~/.bashrc || echo "$GOPATH_EXPORT" >> ~/.bashrc

# -------------------------------
# Install recon tools
# -------------------------------
echo "[+] Installing recon tools..."

install_go_tool() {
    local name="$1"
    local pkg="$2"
    echo "[+] Installing $name..."
    if go install "$pkg" 2>&1; then
        echo "[+] $name installed OK"
    else
        echo "[!] Failed to install $name — check your Go environment"
    fi
}

install_go_tool "subfinder"  "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
install_go_tool "httpx"      "github.com/projectdiscovery/httpx/cmd/httpx@latest"
install_go_tool "gau"        "github.com/lc/gau/v2/cmd/gau@latest"
# FIX: Pin amass to latest stable release tag instead of @master
install_go_tool "amass"      "github.com/owasp-amass/amass/v4/...@v4.2.0"

# -------------------------------
# Verify installation
# -------------------------------
echo ""
echo "[+] Verifying installation..."

ALL_OK=true
for tool in subfinder amass httpx gau nmap; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "[+] $tool OK"
    else
        echo "[!] $tool NOT FOUND — something went wrong"
        ALL_OK=false
    fi
done

echo ""
if [ "$ALL_OK" = true ]; then
    echo "[+] Setup Completed Successfully"
else
    echo "[!] Setup completed with warnings — some tools are missing"
fi

echo ""
echo "Run KAIROX with:"
echo "Give Permission to kairox"
echo "Then Run kairox"
echo "Refer README For More Information"
