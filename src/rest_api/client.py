from dataclasses import dataclass

import aiohttp
import asyncio


# https://docs.aiohttp.org/en/stable/client_quickstart.html

@dataclass
class MyResponse:
    comment: str


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:4000/welcome') as resp:
            print(resp.status)
            print(await resp.text())
            d = await resp.json()  # tu mamy "słownik"
            print(MyResponse(**d))  # tu tworzymy instancję klasy MyResponse


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
