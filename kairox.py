#!/usr/bin/env python3

import os
import sys
import shutil
import tempfile
import subprocess

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# -----------------------------
# ENV FIX (CRITICAL)
# -----------------------------

# Ensure Go tools are always available
go_path = os.path.expanduser("~/go/bin")
if go_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + go_path

# Auto switch to venv if not already
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(BASE_DIR, "venv", "bin", "python")

if os.path.exists(venv_python) and sys.executable != venv_python:
    os.execv(venv_python, [venv_python] + sys.argv)

# -----------------------------
# TOOL INFO
# -----------------------------

TOOL_NAME = "KAIROX"
AUTHOR = "Shadly Maliyekkal"

# -----------------------------
# UI
# -----------------------------

def banner():
    console.print(Panel.fit(
        f"[bold cyan]{TOOL_NAME}[/bold cyan]\n"
        f"[white]Author: {AUTHOR}[/white]",
        border_style="cyan"
    ))

def disclaimer():
    console.print(Panel.fit(
        "[bold red]LEGAL DISCLAIMER[/bold red]\n\n"
        "Use only for authorized security testing.\n"
        "Unauthorized use is illegal.",
        border_style="red"
    ))

def confirm():
    choice = Prompt.ask("[yellow]Proceed? (yes/no)[/yellow]").lower()
    if choice not in ["yes", "y"]:
        console.print("[red]Exiting...[/red]")
        sys.exit()

def get_target():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return Prompt.ask("[cyan]Enter target domain[/cyan]")

# -----------------------------
# DEPENDENCY CHECK
# -----------------------------

def check_tools():
    console.print("\n[cyan]Checking dependencies...[/cyan]\n")

    tools = ["subfinder", "amass", "httpx", "gau", "nmap"]
    missing = []

    for tool in tools:
        if shutil.which(tool):
            console.print(f"[green]{tool} found[/green]")
        else:
            console.print(f"[red]{tool} missing[/red]")
            missing.append(tool)

    if missing:
        console.print("\n[bold red]Missing tools detected[/bold red]")
        console.print("[yellow]Run install.sh first[/yellow]\n")
        sys.exit()

# -----------------------------
# COMMAND RUNNER
# -----------------------------

def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return ""

# -----------------------------
# RECON MODULES
# -----------------------------

def subdomain_enum(domain):
    console.print("\n[cyan]Subdomain Enumeration...[/cyan]")

    subs = set()

    out1 = run_cmd(f"subfinder -silent -d {domain}")
    out2 = run_cmd(f"amass enum -passive -d {domain}")

    for line in (out1 + "\n" + out2).splitlines():
        if line.strip():
            subs.add(line.strip())

    return list(subs)

def live_hosts(subs):
    console.print("\n[cyan]Live Host Detection...[/cyan]")

    if not subs:
        return []

    # FIX: Write to a temp file instead of using shell echo (avoids injection)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("\n".join(subs))
        tmp_path = tmp.name

    try:
        out = run_cmd(f"httpx -silent -status-code -l {tmp_path}")
    finally:
        os.unlink(tmp_path)

    return out.splitlines()

def port_scan(domain):
    console.print("\n[cyan]Port Scanning...[/cyan]")

    out = run_cmd(f"nmap -T4 -F {domain}")

    ports = []
    for line in out.splitlines():
        if "/tcp" in line and "open" in line:
            ports.append(line.strip())

    return ports

def url_mining(domain):
    console.print("\n[cyan]URL Collection...[/cyan]")

    out = run_cmd(f"gau {domain}")

    sensitive = []
    keywords = ["admin", "login", ".env", ".zip", "backup", "api"]

    for url in out.splitlines():
        if any(k in url for k in keywords):
            sensitive.append(url)

    return sensitive[:30]

# -----------------------------
# OUTPUT
# -----------------------------

def show_results(subs, live, ports, urls):
    console.print("\n[bold green]=== RESULTS ===[/bold green]\n")

    console.print("[cyan]Subdomains:[/cyan]")
    for s in subs[:20]:
        console.print(f"- {s}")

    console.print("\n[cyan]Live Hosts:[/cyan]")
    for host in live[:20]:
        console.print(f"- {host}")

    console.print("\n[cyan]Open Ports:[/cyan]")
    for p in ports:
        console.print(f"- {p}")

    console.print("\n[cyan]Sensitive URLs:[/cyan]")
    for u in urls:
        console.print(f"- {u}")

# -----------------------------
# MAIN
# -----------------------------

def main():
    banner()
    disclaimer()
    confirm()

    check_tools()

    target = get_target()
    console.print(f"\n[green]Target: {target}[/green]")

    subs = subdomain_enum(target)
    live = live_hosts(subs)
    ports = port_scan(target)
    urls = url_mining(target)

    show_results(subs, live, ports, urls)

if __name__ == "__main__":
    main()
