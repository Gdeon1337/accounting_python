import asyncio
from typing import List, Set

import aioredis
from aioredis.errors import ConnectionClosedError
from sanic import Sanic
from sanic.exceptions import ServerError


class RedisConn:
    conn = None
    redis_connection = None

    async def create_redis_connection(self, app: Sanic, loop: asyncio.AbstractEventLoop):
        self.redis_connection = app.config.REDIS_CONNECTION
        self.conn = await aioredis.create_redis(self.redis_connection, loop=loop)

    async def close_redis_connection(self, *args):
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()

    async def zadd(self, domains: List, timestamp: int):
        await self.ping()
        pipe = self.conn.pipeline()
        [pipe.zadd('urls', 0, f'{timestamp}:{domain}') for domain in domains]
        await pipe.execute()

    async def zrevrange_by_lex(self, datetime_start: int, datetime_end: int) -> Set:
        await self.ping()
        return await self.conn.zrevrangebylex(
            'urls',
            min=f'{datetime_start-1}'.encode('utf-8'),
            max=f'{datetime_end+1}'.encode('utf-8')
        )

    async def ping(self):
        try:
            await self.conn.ping()
        except ConnectionClosedError:
            raise ConnectionClosedError("Redis conn disconnected")
