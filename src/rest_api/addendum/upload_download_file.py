import asyncio

import aiohttp
import aiofiles


async def download():
    # client download from url
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:4001/serve"
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open('images/served.png', mode='wb')
                await f.write(await resp.read())
                await f.close()


async def upload():
    # client upload to url
    session = aiohttp.ClientSession()
    files = {'file': open('out.png', 'rb')}
    await session.post('http://localhost:4001/upload', data=files)
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(download())
# loop.run_until_complete(upload())

