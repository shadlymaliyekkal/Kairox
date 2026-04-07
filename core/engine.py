import asyncio
from modules.subdomain import get_subdomains
from modules.live import get_live
from modules.ports import scan_ports
from modules.urls import get_urls
from core.analyzer import classify

async def run_engine(domain):
    subs = await get_subdomains(domain)
    categories = classify(subs)

    live_task = get_live(subs)
    port_task = scan_ports(domain)
    url_task = get_urls(domain)

    live, ports, urls = await asyncio.gather(
        live_task, port_task, url_task
    )

    return categories, live, ports, urls