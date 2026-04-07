from utils.runner import run_cmd

async def get_urls(domain):
    output = await run_cmd(f"gau {domain}")

    sensitive = []
    for url in output.splitlines():
        if any(x in url for x in ["admin", "login", ".zip", ".env", "backup", "api"]):
            sensitive.append(url)

    return sensitive[:50]