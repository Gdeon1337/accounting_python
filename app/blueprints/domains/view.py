from datetime import datetime

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from app.helpers import redis_loaders
# from sanic_openapi import doc  # pylint: disable=wrong-import-order
from app.helpers.validators import raise_if_empty, raise_if_not_int


blueprint = Blueprint('domains', url_prefix='/domains', strict_slashes=True)


# @doc.summary('Добавление домейнов')
# @doc.response(200, {"status": doc.String("статус")})
@blueprint.post('')
async def domain(request: Request):
    links = request.json.get('links')
    raise_if_empty(links)
    response = await redis_loaders.create_domains(links, int(datetime.now().timestamp()))
    return json(response)


# @doc.summary('Получение домейнов')
# @doc.security(True)
# @doc.response(200, swagger_models.Currency)
@blueprint.get('')
async def get_currency(request: Request):
    date_time_start = request.args.get('from')
    date_time_end = request.args.get('to')
    raise_if_empty(date_time_end, date_time_start)
    raise_if_not_int(date_time_end, date_time_start)
    domains = await redis_loaders.get_list_domains(int(date_time_start), int(date_time_end))
    return json({'domains': domains, 'status': 'ok'})
