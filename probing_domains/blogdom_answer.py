#!/usr/bin/env python3
"""
asyncio.getaddrinfo():
The asyncio.getaddrinfo() coroutine is an asynchronous version of the standard,
blocking socket.getaddrinfo() function, used to convert a hostname and port number
into a list of socket address information tuples.

memory efficiency with generators:
Generators produce values on-demand, while list comprehensions create all values
upfront in memory.


"""

import asyncio
import socket
from keyword import kwlist
from typing import Tuple

MAX_KEYWORD_LEN = 4


async def probe(domain: str) -> Tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:

        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f"{name}.dev".lower() for name in names)
    coros = [probe(domain) for domain in domains]
    for coro in asyncio.as_completed(coros):
        domain, found = await coro
        mark = "+" if found else ""
        print(f"{mark} {domain}")
