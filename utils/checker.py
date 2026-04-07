import shutil
import sys
from rich.console import Console

console = Console()

def check_tools():
    tools = ["subfinder", "amass", "httpx", "gau", "nmap"]
    console.print("\n[cyan]Checking dependencies...[/cyan]\n")

    missing = []
    for t in tools:
        if shutil.which(t):
            console.print(f"[green]{t} found[/green]")
        else:
            console.print(f"[red]{t} missing[/red]")
            missing.append(t)

    if missing:
        console.print("\n[red]Run install.sh before using KAIROX[/red]")
        sys.exit()