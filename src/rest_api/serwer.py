from asyncio import sleep
from dataclasses import dataclass
from os import getenv
from random import randint
from uuid import uuid4, UUID

import aiohttp_cors
import asyncpg
from aiohttp import web
from aiohttp.abc import Application
from dotenv import load_dotenv

routes = web.RouteTableDef()
app = web.Application()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


async def blah():
    await sleep(1.3)


@routes.get('/')
async def hello(request):
    await blah()
    return web.json_response({'comment': 'OK'})


@routes.get('/welcome')
async def hello(request):
    return web.json_response({'comment': 'Welcome!'})


@routes.get('/square')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/square?x=12
    sx: str = request.rel_url.query['x']
    x = int(sx)
    xx = x ** 2
    return web.json_response({'result': xx})


@routes.get('/user')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/user?name=Radek
    name: str = request.rel_url.query['name']

    # sposób na wykorzystanie metod serwisu bazodanowego
    user = await app['db'].get_user_by_name(name=name)

    return web.json_response(user.__dict__)  # można zwrócić list[dict] etc..


@dataclass
class User:
    id: int
    name: str


load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:
    # to jest prototyp klasy z dostępem do bazy danych -- todo rozwinąć go jak dotychczas

    async def initialize(self):
        # self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, min_size=15, max_size=20,
        #                                       server_settings={'search_path': SCHEMA})

        print('connected!')

    async def foo(self):
        await sleep(0.5)
        return User(id=123, name='Xiaomi')

    async def get_user_by_name(self, name: str):
        return User(id=123, name=name)


async def app_factory():
    db = DbService()
    await db.initialize()
    app.add_routes(routes)
    app['db'] = db
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=4000)
