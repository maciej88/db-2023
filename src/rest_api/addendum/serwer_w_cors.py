from asyncio import sleep

import aiohttp_cors
from aiohttp import web
from aiohttp.abc import BaseRequest

routes = web.RouteTableDef()

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


@routes.get('/welcome/{id}')
async def hello(request):
    print('from get')
    return web.json_response({'comment': 'Welcome!'})


@routes.put('/welcome/{id}')
async def hellx(request):
    print('from put')
    return web.json_response({'comment': 'Welcome!'})


@routes.get('/square')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/square?x=12
    sx: str = request.rel_url.query['x']
    x = int(sx)
    xx = x ** 2
    return web.json_response({'result': xx})


@routes.post('/upload')
async def accept_file(req: BaseRequest):
    # https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
    print('file upload request hit...')
    reader = await req.multipart()

    # field = await reader.next()
    # name = await field.read(decode=True)

    field = await reader.next()
    assert field.name == 'file'
    print(f'read field object: {field}')
    filename = field.filename
    # Cannot rely on Content-Length if transfer is chunked.
    print(f'filename:{filename}')
    filename = 'images/' + filename
    size = 0
    with open(filename, 'wb') as f:
        file_as_bytes = b''
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            print(type(chunk))
            if not chunk:
                break
            size += len(chunk)
            file_as_bytes += chunk
            # f.write(chunk)
        f.write(file_as_bytes)

    return web.json_response({'name': filename, 'size': size})


@routes.get('/serve')
async def serve_file(req: BaseRequest):
    return web.FileResponse('out.png')


#  setup generous CORS:
app = web.Application()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

app.router.add_routes(routes)

print(app.router.routes())

for route in list(app.router.routes()):
    # print(f'adding {route}')
    cors.add(route)


async def starter():
    """
    Starter / app factory, czyli miejsce gdzie można inicjalizować asynchronicze konstrukty.

    :return:
    """
    await sleep(0.2)
    print('app is starting..')
    return app


if __name__ == '__main__':
    web.run_app(starter(), port=4001)
