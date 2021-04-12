from aiohttp import web
from app import routes

webapp = web.Application()
webapp.add_routes(routes.get())
