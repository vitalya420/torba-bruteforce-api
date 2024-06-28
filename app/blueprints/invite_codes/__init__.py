from sanic import Blueprint

invite_codes = Blueprint('invite_codes', url_prefix='invite_codes', version_prefix='api/v', version=1)

from . import views
