#!/usr/bin/env python3
from aiohttp import web

from ws_factorial_service.api import API


app = web.Application()
ws_api = API(app)
app.add_routes([web.get('/', ws_api.handle)])


if __name__ == '__main__':
    web.run_app(app)
