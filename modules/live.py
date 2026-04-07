from utils.runner import run_cmd

async def get_live(subs):
    cmd = "echo '{}' | httpx -silent -status-code -title".format("\n".join(subs))
    output = await run_cmd(cmd)

    results = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            results.append({
                "url": parts[0],
                "status": parts[1]
            })

    return results