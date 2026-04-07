#!/usr/bin/env python3

import os
import sys
import shutil
import time
import random
import tempfile
import subprocess
import threading

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.columns import Columns
from rich import box
from rich.progress import (
    Progress, SpinnerColumn, BarColumn,
    TextColumn, TimeElapsedColumn, TaskProgressColumn
)

console = Console()

# -----------------------------
# ENV FIX (CRITICAL)
# -----------------------------

go_path = os.path.expanduser("~/go/bin")
if go_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + go_path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(BASE_DIR, "venv", "bin", "python")

if os.path.exists(venv_python) and sys.executable != venv_python:
    os.execv(venv_python, [venv_python] + sys.argv)

# -----------------------------
# TOOL INFO
# -----------------------------

TOOL_NAME = "KAIROX"
AUTHOR    = "Shadly Maliyekkal"
VERSION   = "2.0"

# -----------------------------
# ASCII ART BANNER
# -----------------------------

KAIROX_ASCII = r"""
██╗  ██╗ █████╗ ██╗██████╗  ██████╗ ██╗  ██╗
██║ ██╔╝██╔══██╗██║██╔══██╗██╔═══██╗╚██╗██╔╝
█████╔╝ ███████║██║██████╔╝██║   ██║ ╚███╔╝ 
██╔═██╗ ██╔══██║██║██╔══██╗██║   ██║ ██╔██╗ 
██║  ██╗██║  ██║██║██║  ██║╚██████╔╝██╔╝ ██╗
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
"""

CYBER_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*<>/\\|[]{}!?"

# Gradient: neon-green → cyan → electric-blue
GRADIENT_COLORS = [
    "#00ff41", "#00f550", "#00eb5e", "#00e06d",
    "#00d07c", "#00bf8a", "#00ad99", "#00c8c8",
    "#00b8e0", "#00a8f5", "#0096ff", "#0080ff",
]

# -----------------------------
# ANIMATIONS
# -----------------------------

def matrix_glitch_banner():
    """Render the banner with a matrix-glitch reveal effect."""
    lines = KAIROX_ASCII.strip("\n").split("\n")
    width = max(len(l) for l in lines)
    total_frames = 20

    with Live(console=console, refresh_per_second=24) as live:
        for frame in range(total_frames + 1):
            reveal_ratio = frame / total_frames
            text = Text()
            for line in lines:
                chars = list(line.ljust(width))
                n = max(len(chars), 1)
                for i, ch in enumerate(chars):
                    if ch == " ":
                        text.append(" ")
                        continue
                    reveal_threshold = i / n
                    if reveal_ratio >= reveal_threshold:
                        # Settled — neon gradient
                        color_idx = int(i / n * (len(GRADIENT_COLORS) - 1))
                        text.append(ch, style=f"bold {GRADIENT_COLORS[color_idx]}")
                    elif reveal_ratio >= reveal_threshold - 0.15:
                        # Glitching — random char
                        text.append(random.choice(CYBER_CHARS), style="bold #00ff41")
                    else:
                        # Not reached — dim block noise
                        text.append(random.choice("░▒▓"), style="dim #003300")
                text.append("\n")
            live.update(text)
            time.sleep(0.055)


def type_line(text: str, style: str = "bold #00ff41", delay: float = 0.03):
    """Typewriter effect for a single line."""
    for ch in text:
        console.print(ch, style=style, end="")
        time.sleep(delay)
    console.print()


def scan_line_effect(label: str, duration: float = 1.0):
    """Horizontal scan-bar animation."""
    width = 48
    steps = 28
    with Live(console=console, refresh_per_second=30) as live:
        for step in range(steps + 1):
            pos = int(step / steps * width)
            bar = (
                "[bold #00aa00]" + "━" * pos + "[/bold #00aa00]"
                "[bold #00ff41]▶[/bold #00ff41]"
                "[dim #001a00]" + "━" * (width - pos) + "[/dim #001a00]"
            )
            live.update(Text.from_markup(f"  {label}  {bar}"))
            time.sleep(duration / steps)


def glitch_label(text: str, cycles: int = 7):
    """Glitch-resolve a label before settling."""
    with Live(console=console, refresh_per_second=20) as live:
        for i in range(cycles):
            if i < cycles - 1:
                glitched = "".join(
                    random.choice(CYBER_CHARS) if random.random() > 0.45 else c
                    for c in text
                )
                live.update(Text(glitched, style="bold #00ff99"))
            else:
                live.update(Text(text, style="bold #00ffff"))
            time.sleep(0.07)


def hacker_progress(tasks: list) -> dict:
    """
    Run a list of (label, callable) pairs with a stylised
    animated progress bar. Returns {label: result}.
    """
    results = {}
    with Progress(
        SpinnerColumn(spinner_name="dots2", style="bold #00ff41"),
        TextColumn("[bold #00ccff]{task.description}"),
        BarColumn(
            bar_width=36,
            style="#003300",
            complete_style="#00ff41",
            finished_style="#00ffaa",
        ),
        TaskProgressColumn(style="#00ff99"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        for label, fn in tasks:
            task_id = progress.add_task(label, total=100)
            container = {}

            def worker(f=fn, c=container):
                c["result"] = f()

            t = threading.Thread(target=worker, daemon=True)
            t.start()

            ticks = 0
            while t.is_alive():
                if ticks < 30:
                    inc = random.randint(2, 5)
                elif ticks < 70:
                    inc = random.randint(0, 2)
                else:
                    inc = random.randint(1, 4)
                advance = min(inc, 99 - ticks)
                progress.advance(task_id, advance)
                ticks = min(ticks + advance, 99)
                time.sleep(0.07)

            t.join()
            progress.update(task_id, completed=100)
            results[label] = container.get("result", [])

    return results

# -----------------------------
# UI
# -----------------------------

def banner():
    matrix_glitch_banner()
    console.print()

    subtitle = Text()
    subtitle.append("  ⚡ ", style="#ffff00")
    subtitle.append("Advanced Reconnaissance Framework", style="bold #00ccff")
    subtitle.append("  ⚡", style="#ffff00")
    console.print(subtitle, justify="center")

    meta = Text()
    meta.append(f"  v{VERSION}  ", style="bold #ff6600")
    meta.append("│", style="dim #555555")
    meta.append(f"  {AUTHOR}  ", style="bold #00ff99")
    meta.append("│", style="dim #555555")
    meta.append("  Authorized Use Only  ", style="bold #ff4444")
    console.print(meta, justify="center")
    console.print()


def disclaimer():
    text = Text()
    text.append("⚠  LEGAL DISCLAIMER  ⚠\n\n", style="bold #ff3333")
    text.append("This tool is for ", style="#cccccc")
    text.append("authorized security testing ONLY", style="bold #ff6600")
    text.append(".\nUnauthorized use is ", style="#cccccc")
    text.append("illegal and unethical", style="bold #ff3333")
    text.append(".", style="#cccccc")

    console.print(Panel(
        text,
        border_style="#ff3333",
        padding=(1, 4),
        expand=False,
    ))
    console.print()


def confirm():
    glitch_label("[ AUTHORIZATION REQUIRED ]")
    console.print()
    choice = Prompt.ask(
        "[bold #ffff00]  Proceed with authorized target?[/bold #ffff00] [dim](yes/no)[/dim]"
    ).lower()
    if choice not in ["yes", "y"]:
        type_line("\n  [ SESSION TERMINATED ]", style="bold #ff3333", delay=0.05)
        sys.exit()
    console.print()
    scan_line_effect("INITIALIZING", duration=0.8)
    console.print()


def get_target():
    if len(sys.argv) > 1:
        return sys.argv[1]
    console.print()
    return Prompt.ask("[bold #00ff41]  ⌖  TARGET DOMAIN[/bold #00ff41]")

# -----------------------------
# DEPENDENCY CHECK
# -----------------------------

def check_tools():
    console.print("\n[bold #00ccff]  ◈  DEPENDENCY CHECK[/bold #00ccff]\n")

    tools = ["subfinder", "amass", "httpx", "gau", "nmap"]
    missing = []

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="dim #555555", width=3)
    table.add_column(width=14)
    table.add_column()

    for tool in tools:
        if shutil.which(tool):
            table.add_row("▶", f"[bold #00ff99]{tool}[/bold #00ff99]", "[bold #00ff41]FOUND  ✓[/bold #00ff41]")
        else:
            table.add_row("▶", f"[bold #ff6644]{tool}[/bold #ff6644]", "[bold #ff3333]MISSING ✗[/bold #ff3333]")
            missing.append(tool)

    console.print(table)

    if missing:
        console.print(f"\n[bold #ff3333]  Missing: {', '.join(missing)}[/bold #ff3333]")
        console.print("[#ffaa00]  Run ./install.sh first[/#ffaa00]\n")
        sys.exit()

# -----------------------------
# COMMAND RUNNER
# -----------------------------

def run_cmd(cmd: str) -> str:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""

# -----------------------------
# RECON MODULES
# -----------------------------

def subdomain_enum(domain: str) -> list:
    subs = set()
    out1 = run_cmd(f"subfinder -silent -d {domain}")
    out2 = run_cmd(f"amass enum -passive -d {domain}")
    for line in (out1 + "\n" + out2).splitlines():
        if line.strip():
            subs.add(line.strip())
    return list(subs)


def live_hosts(subs: list) -> list:
    if not subs:
        return []
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("\n".join(subs))
        tmp_path = tmp.name
    try:
        out = run_cmd(f"httpx -silent -status-code -l {tmp_path}")
    finally:
        os.unlink(tmp_path)
    return out.splitlines()


def port_scan(domain: str) -> list:
    out = run_cmd(f"nmap -T4 -F {domain}")
    return [
        line.strip() for line in out.splitlines()
        if "/tcp" in line and "open" in line
    ]


def url_mining(domain: str) -> list:
    out = run_cmd(f"gau {domain}")
    keywords = ["admin", "login", ".env", ".zip", "backup", "api"]
    return [url for url in out.splitlines() if any(k in url for k in keywords)][:30]

# -----------------------------
# OUTPUT
# -----------------------------

def show_results(subs, live, ports, urls):
    console.print()
    scan_line_effect("COMPILING RESULTS", duration=0.5)
    console.print()

    def make_table(title, items, color, icon):
        display = items if items else ["[dim #555555]no results[/dim #555555]"]
        t = Table(
            title=f"{icon}  {title}",
            title_style=f"bold {color}",
            box=box.MINIMAL,
            border_style="dim #2a2a2a",
            show_header=False,
            padding=(0, 2),
            expand=False,
        )
        t.add_column(style=color)
        for item in display:
            t.add_row(item)
        return t

    sub_table  = make_table("SUBDOMAINS",     [s for s in subs[:20]],  "#00ff99", "◈")
    live_table = make_table("LIVE HOSTS",     live[:20],                "#00ccff", "◉")
    port_table = make_table("OPEN PORTS",     ports,                    "#ff9900", "◆")
    url_table  = make_table("SENSITIVE URLs", urls,                     "#ff4466", "◎")

    console.print(Columns([sub_table, live_table], equal=True, expand=True))
    console.print()
    console.print(Columns([port_table, url_table], equal=True, expand=True))
    console.print()

    summary = Text()
    summary.append("  ✓ SCAN COMPLETE  ", style="bold #00ff41 on #001a00")
    summary.append(f"   {len(subs)} subdomains  ", style="bold #00ff99")
    summary.append("│", style="dim #444444")
    summary.append(f"  {len(live)} live hosts  ", style="bold #00ccff")
    summary.append("│", style="dim #444444")
    summary.append(f"  {len(ports)} open ports  ", style="bold #ff9900")
    summary.append("│", style="dim #444444")
    summary.append(f"  {len(urls)} sensitive URLs  ", style="bold #ff4466")

    console.print(Panel(summary, border_style="#00ff41", padding=(0, 2), expand=False))
    console.print()

# -----------------------------
# MAIN
# -----------------------------

def main():
    banner()
    disclaimer()
    confirm()
    check_tools()

    target = get_target()
    console.print(
        f"\n[bold #ffff00]  ⌖  TARGET LOCKED[/bold #ffff00] "
        f"[dim #555555]→[/dim #555555] "
        f"[bold #ff6600]{target}[/bold #ff6600]\n"
    )

    # Recon phases — each runs in a background thread with live progress
    subs_cache = {}

    def run_subs():
        subs_cache["subs"] = subdomain_enum(target)
        return subs_cache["subs"]

    def run_live():
        # Reuse already-fetched subs if available
        base = subs_cache.get("subs") or subdomain_enum(target)
        return live_hosts(base)

    recon_tasks = [
        ("Subdomain Enumeration ", run_subs),
        ("Live Host Detection   ", run_live),
        ("Port Scanning         ", lambda: port_scan(target)),
        ("URL Mining            ", lambda: url_mining(target)),
    ]

    results = hacker_progress(recon_tasks)

    show_results(
        results["Subdomain Enumeration "],
        results["Live Host Detection   "],
        results["Port Scanning         "],
        results["URL Mining            "],
    )


if __name__ == "__main__":
    main()
