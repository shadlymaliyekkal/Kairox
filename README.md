# KAIROX

KAIROX is a reconnaissance intelligence tool designed to automate and organize attack surface discovery with structured, readable output.

It integrates multiple reconnaissance techniques and tools into a single workflow, providing categorized and prioritized results for security testing.

---

## FEATURES

* Subdomain Enumeration (passive + aggregated)
* Live Host Detection
* Port Scanning
* URL & Endpoint Mining
* Sensitive Data Filtering
* Categorized Output (High / Medium / Low value)
* Clean Terminal Interface

---

## INSTALLATION

### 1. Clone the repository

git clone https://github.com/yourname/kairox.git
cd kairox

### 2. Run installer

sed -i 's/\r$//' install.sh && chmod +x install.sh && ./install.sh

This installs:

* Python dependencies
* Required external recon tools
* System packages

---

## USAGE
chmod +x kairox

Run kairox

### Steps

* Accept legal disclaimer
* Enter target domain
* View results

---

## OUTPUT SECTIONS

* High Value Targets
* Medium Value Targets
* Live Hosts
* Open Ports
* Sensitive URLs

---

## PROJECT STRUCTURE

kairox/
├── kairox.py
├── core/
├── modules/
├── utils/
└── output/

---

## DISCLAIMER

This tool is intended for **authorized security testing and educational purposes only**.

Unauthorized use is illegal.

The author is not responsible for misuse or any damage caused.

---

## AUTHOR

**Shadly Maliyekkal**

---

## LICENSE

MIT License
