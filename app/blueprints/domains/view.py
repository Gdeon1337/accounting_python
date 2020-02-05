from datetime import datetime

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from app.helpers import redis_loaders
from app.helpers.validators import raise_if_empty, raise_if_not_int


blueprint = Blueprint('domains', url_prefix='/', strict_slashes=True)


@blueprint.post('/visited_links')
async def domain(request: Request):
    links = request.json.get('links')
    raise_if_empty(links)
    await redis_loaders.create_domains(links, int(datetime.now().timestamp()))
    return json({'status': 'ok'})


@blueprint.get('/visited_domains')
async def get_currency(request: Request):
    date_time_start = request.args.get('from')
    date_time_end = request.args.get('to')
    raise_if_empty(date_time_end, date_time_start)
    raise_if_not_int(date_time_end, date_time_start)
    domains = await redis_loaders.get_list_domains(int(date_time_start), int(date_time_end))
    return json({'domains': domains, 'status': 'ok'})
