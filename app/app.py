from sanic import Blueprint, Sanic

from . import config
from .blueprints import blueprint


def create_app(config_object: object = config.Config) -> Sanic:
    app = Sanic()
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Sanic):
    from . import extensions
    extensions.register_redis(app)
    # extensions.register_openapi(app)


def register_blueprints(app: Sanic):
    app.blueprint(blueprint)
