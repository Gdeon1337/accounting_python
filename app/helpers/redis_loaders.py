import re
from typing import Dict, List, Set

from app.extensions import conn


re_domain = re.compile(r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,65}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}')
re_ref_domain = re.compile(r'^\d*\:')


def get_domain(domain: str):
    result = re_domain.search(domain)
    if result:
        return result.group(0)
    return None


def validator_domains(domains: List):
    return [get_domain(domain) for domain in domains if get_domain(domain)]


async def create_domains(domains: List, timestamp: int) -> Dict:
    await conn.zadd(validator_domains(domains), timestamp)
    return {'status': 'ok'}


async def get_list_domains(datetime_start: int, datetime_end: int) -> Set:
    domains = await conn.zrevrange_by_lex(datetime_start, datetime_end)
    return {re_ref_domain.sub('', domain.decode()) for domain in domains}
