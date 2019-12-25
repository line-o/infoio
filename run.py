from aiohttp import web
from infoschild import Infoschild
try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio

async def handleStats(request):
    text = "hope is at: " + str(infoschild.getHope())
    return web.Response(text=text)

async def handleHope(request):
    app['infoschild'].setHope(1)
    location = request.app.router['stats'].url_for()
    raise web.HTTPFound(location=location)

async def handleDestruction(request):
    app['infoschild'].setHope(-1)
    location = request.app.router['stats'].url_for()
    raise web.HTTPFound(location=location)

# async def wshandle(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)

#     async for msg in ws:
#         if msg.type == web.WSMsgType.text:
#             await ws.send_str("Hello, {}".format(msg.data))
#         elif msg.type == web.WSMsgType.binary:
#             await ws.send_bytes(msg.data)
#         elif msg.type == web.WSMsgType.close:
#             break

#     return ws

HOST = '0.0.0.0'
PORT = 80

path_to_static_folder = './static'
infoschild = Infoschild()

app = web.Application()
app['infoschild'] = infoschild
app.add_routes([web.get('/', handleStats, name='stats'),
                web.get('/hope', handleHope),
                web.get('/destruction', handleDestruction)
                # , web.static('/static', path_to_static_folder)
                ])

loop = asyncio.get_event_loop()
# add stuff to the loop
loop.call_at(1.0, infoschild.step, loop)
# set up aiohttp - like run_app, but non-blocking
runner = web.AppRunner(app)
loop.run_until_complete(runner.setup())
site = web.TCPSite(runner, HOST, PORT)    
loop.run_until_complete(site.start())

# add more stuff to the loop

loop.run_forever()
loop.close()
