from app.extensions import conn
from typing import List


async def create_domains(domains: List, timestamp: int):
    await conn.zadd(domains, timestamp)
