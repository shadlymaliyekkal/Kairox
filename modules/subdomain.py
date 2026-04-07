from utils.runner import run_cmd

async def get_subdomains(domain):
    cmds = [
        f"subfinder -silent -d {domain}",
        f"amass enum -passive -d {domain}"
    ]

    results = await asyncio.gather(*(run_cmd(c) for c in cmds))

    subs = set()
    for r in results:
        for line in r.splitlines():
            subs.add(line.strip())

    return list(subs)