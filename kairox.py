#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# -----------------------------

# Auto environment handling

# -----------------------------

# Fix PATH for Go tools

os.environ["PATH"] += os.pathsep + os.path.expanduser("~/go/bin")

# Auto switch to venv if not already

venv_python = os.path.join(os.path.dirname(**file**), "venv", "bin", "python")
if sys.executable != venv_python and os.path.exists(venv_python):
os.execv(venv_python, [venv_python] + sys.argv)

# -----------------------------

# Tool Info

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
while True:
choice = Prompt.ask("[yellow]Proceed? (yes/no)[/yellow]").lower()
if choice in ["yes", "y"]:
return
elif choice in ["no", "n"]:
console.print("[red]Exiting...[/red]")
sys.exit()
else:
console.print("[red]Invalid input[/red]")

def get_target():
if len(sys.argv) > 1:
return sys.argv[1]
return Prompt.ask("[cyan]Enter target domain[/cyan]")

# -----------------------------

# Dependency Check

# -----------------------------

def check_tools():
console.print("\n[cyan]Checking dependencies...[/cyan]\n")

```
tools = ["subfinder", "amass", "httpx", "gau", "nmap"]
missing = []

for tool in tools:
    if shutil.which(tool):
        console.print(f"[green]{tool} found[/green]")
    else:
        console.print(f"[red]{tool} missing[/red]")
        missing.append(tool)

if missing:
    console.print("\n[red]Missing tools detected[/red]")
    console.print("[yellow]Run install.sh first[/yellow]\n")
    sys.exit()
```

# -----------------------------

# Recon Functions

# -----------------------------

def run_cmd(cmd):
try:
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
return result.stdout.strip()
except Exception:
return ""

def subdomain_enum(domain):
console.print("\n[cyan]Running subdomain enumeration...[/cyan]")

```
subs = set()

output1 = run_cmd(f"subfinder -silent -d {domain}")
output2 = run_cmd(f"amass enum -passive -d {domain}")

for line in (output1 + "\n" + output2).splitlines():
    if line.strip():
        subs.add(line.strip())

return list(subs)
```

def live_hosts(subs):
console.print("\n[cyan]Checking live hosts...[/cyan]")

```
data = "\n".join(subs)
output = run_cmd(f"echo '{data}' | httpx -silent -status-code")

return output.splitlines()
```

def url_mining(domain):
console.print("\n[cyan]Collecting URLs...[/cyan]")

```
output = run_cmd(f"gau {domain}")

sensitive = []
for url in output.splitlines():
    if any(x in url for x in ["admin", "login", ".zip", ".env", "backup", "api"]):
        sensitive.append(url)

return sensitive[:30]
```

def port_scan(domain):
console.print("\n[cyan]Scanning ports...[/cyan]")

```
output = run_cmd(f"nmap -T4 -F {domain}")

ports = []
for line in output.splitlines():
    if "/tcp" in line and "open" in line:
        ports.append(line.strip())

return ports
```

# -----------------------------

# Output

# -----------------------------

def show_results(subs, live, ports, urls):
console.print("\n[bold green]--- RESULTS ---[/bold green]\n")

```
console.print("[cyan]Subdomains:[/cyan]")
for s in subs[:20]:
    console.print(f"- {s}")

console.print("\n[cyan]Live Hosts:[/cyan]")
for l in live[:20]:
    console.print(f"- {l}")

console.print("\n[cyan]Open Ports:[/cyan]")
for p in ports:
    console.print(f"- {p}")

console.print("\n[cyan]Sensitive URLs:[/cyan]")
for u in urls:
    console.print(f"- {u}")
```

# -----------------------------

# Main

# -----------------------------

def main():
banner()
disclaimer()
confirm()

```
check_tools()

target = get_target()
console.print(f"\n[green]Target: {target}[/green]")

subs = subdomain_enum(target)
live = live_hosts(subs)
ports = port_scan(target)
urls = url_mining(target)

show_results(subs, live, ports, urls)
```

if **name** == "**main**":
main()
