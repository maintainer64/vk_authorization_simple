import aiohttp


async def session_maker() -> aiohttp.TCPConnector:
    return aiohttp.TCPConnector(ssl=False)
