import asyncio
from httpx import AsyncClient
from typing import List


def download_many(cc_list: List[str]) -> int:
    return asyncio.run(supervisor(cc_list))


async def supervisor(cc_list: List[str]) -> int:
    async with AsyncClient() as client:
        todo = [download_one(client, cc) for cc in sorted(cc_list)]
        res = await asyncio.gather(*todo)
    return len(res)


if __name__ == "__main__":
    main(download_many)
