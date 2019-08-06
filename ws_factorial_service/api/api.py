import json
import weakref

import aiohttp

from .dispatch import Dispatcher
from .errors import UnknownMethod


class API:

    def __init__(self, app, dispatcher=None):
        self.dispatcher = dispatcher or Dispatcher()
        self._init_app(app)

    @staticmethod
    async def _on_shutdown(app):
        for ws in set(app['websockets']):
            await ws.close(
                code=aiohttp.WSCloseCode.GOING_AWAY,
                message='Server shutdown',
            )

    def _init_app(self, app):
        app['websockets'] = weakref.WeakSet()
        app.on_shutdown.append(self._on_shutdown)

    async def handle(self, request):
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        request.app['websockets'].add(ws)
        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    response = await self._handle_api_request(msg.data)
                    await ws.send_str(json.dumps(response))
                if msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR):
                    break
        finally:
            request.app['websockets'].discard(ws)
        return ws

    async def _handle_api_request(self, data):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return {
                'response': {
                    'error': 'Failed to parse request',
                },
            }
        try:
            method_name = data['method']
        except KeyError:
            return {
                'response': {
                    'error': 'No method specified',
                }
            }
        payload = data.get('payload')
        try:
            result = await self.dispatcher.dispatch(method_name, payload)
        except UnknownMethod as exc:
            return {
                'method': method_name,
                'response': {
                    'error': f'Unknown method: {exc.method_name}',
                }
            }
        except Exception:
            return {
                'method': method_name,
                'response': {
                    'error': 'Unknown error',
                }
            }
        return {
            'method': method_name,
            'response': {
                'result': result,
            },
        }
