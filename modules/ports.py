from utils.runner import run_cmd

async def scan_ports(domain):
    output = await run_cmd(f"nmap -T4 -F {domain}")

    ports = []
    for line in output.splitlines():
        if "/tcp" in line and "open" in line:
            ports.append(line.strip())

    return ports