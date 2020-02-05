from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import InvalidUsage
from aioredis.errors import ConnectionClosedError


blueprint_exceptions = Blueprint('except', url_prefix='/', strict_slashes=True)


@blueprint_exceptions.exception(InvalidUsage)
def except_invalid_usage(requests: Request, exceptions):
    return json({
        'status': str(exceptions)
    }, status=400)


@blueprint_exceptions.exception(ConnectionClosedError)
def except_connect_error(requests: Request, exceptions):
    return json({
        'status': str(exceptions)
    }, status=500)
