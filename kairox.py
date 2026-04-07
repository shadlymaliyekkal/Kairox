import os
import sys
import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.rule import Rule

from utils.checker import check_tools
from core.engine import run_engine

console = Console()

TOOL_NAME = "KAIROX"
AUTHOR = "Shadly Maliyekkal"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    console.print(Panel.fit(
        f"[bold #00d4ff]{TOOL_NAME}[/bold #00d4ff]\n"
        f"[white]Author: {AUTHOR}[/white]",
        border_style="#00d4ff"
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
        c = Prompt.ask("[yellow]Proceed? (yes/no)[/yellow]").lower()
        if c in ["yes", "y"]:
            return
        elif c in ["no", "n"]:
            sys.exit()
        else:
            console.print("[red]Invalid input[/red]")

def get_target():
    t = Prompt.ask("[cyan]Enter target domain[/cyan]")
    if not t.strip():
        sys.exit()
    return t.strip()

def show(data, live, ports, urls):
    console.print(Rule("[bold cyan]Results[/bold cyan]"))

    def render(title, items, color):
        table = Table(title=title, style=color)
        table.add_column("Value")
        for i in items[:20]:
            table.add_row(str(i))
        console.print(table)

    render("High Value", data["high"], "red")
    render("Medium Value", data["medium"], "yellow")
    render("Live Hosts", [f"{l['url']} [{l['status']}]" for l in live], "cyan")
    render("Open Ports", ports, "green")
    render("Sensitive URLs", urls, "magenta")

    console.print(Rule("[green]Completed[/green]"))

def main():
    clear()
    banner()
    disclaimer()
    confirm()

    check_tools()

    target = get_target()
    console.print(f"[green]Target: {target}[/green]\n")

    data, live, ports, urls = asyncio.run(run_engine(target))
    show(data, live, ports, urls)

if __name__ == "__main__":
    main()