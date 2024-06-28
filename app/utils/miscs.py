import inspect
from datetime import datetime, UTC


def get_utc_now():
    return int(datetime.now(tz=UTC).timestamp())


def is_sync_function(func):
    return inspect.isfunction(func) and not inspect.iscoroutinefunction(func)


def namedtuple2dict(instance):
    return {field: getattr(instance, field) for field in instance._fields}
