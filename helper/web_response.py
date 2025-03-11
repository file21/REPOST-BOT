# +++ Made By King [telegram username: @Shidoteshika1] +++

from aiohttp import web

routes = web.RouteTableDef()

#router
@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("re-post-link-gen-bot")

#responding web server using router
async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app