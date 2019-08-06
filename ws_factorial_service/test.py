#!/usr/bin/env python3
import asyncio
import json

import aiohttp


async def run_test(msg, expected_answer):
    async with aiohttp.ClientSession().ws_connect('http://localhost:8080') as ws:
        await ws.send_str(json.dumps(msg))
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if json.loads(msg.data) == expected_answer:
                    await ws.close()
                    print('OK')
                    break
            print(f'Fail, received: {msg}, expected: {expected_answer}')
            break
    await ws.close()


async def test_it():
    await run_test(
        {'method': 'factorial', 'payload': {'value': 5}},
        {'method': 'factorial', 'response': {'result': 120}},
    )
    await run_test(
        {'method': 'factorial', 'payload': {'value': 6}},
        {'method': 'factorial', 'response': {'result': 720}},
    )
    await run_test(
        {},
        {'response': {'error': 'No method specified'}},
    )
    await run_test(
        {'method': 'foo'},
        {'method': 'foo', 'response': {'error': 'Unknown method: foo'}},
    )
    await run_test(
        {'method': 'factorial'},
        {'method': 'factorial', 'response': {'error': 'Unknown error'}},
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_it())
