from sanic import Blueprint

users = Blueprint('users', url_prefix='users', version_prefix='api/v', version=1)

from . import views
