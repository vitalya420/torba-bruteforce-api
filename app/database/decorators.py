import inspect
import types
from functools import wraps
from typing import get_type_hints, Union, Sequence, Optional, Coroutine, Awaitable

from app.database.exceptions import RecordNotFound


def query_file(name: str, commit_after: bool = False, cursor_callback=None):
    def wrapper(func):
        @wraps(func)
        async def decorator(*args, **kwargs):
            sig = inspect.signature(func)

            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            params = bound_args.arguments

            db_instance = args[0]

            params.pop('self', None)

            cursor = await db_instance.execute(name, params, commit=commit_after)
            if cursor_callback:
                return await cursor_callback(cursor)

            type_hints = get_type_hints(func)
            return_type = type_hints.get('return')

            if return_type is None:
                return None

            none_allowed = getattr(return_type, "__origin__", None) == Union and types.NoneType in return_type.__args__

            if getattr(return_type, "__origin__", None) == Union:
                expected_types = tuple(type_ for type_ in return_type.__args__ if type_ is not types.NoneType)
                if len(expected_types) > 1:
                    raise RecordNotFound("Can not decide which type to return")
                expected_type, = expected_types
            else:
                expected_type = return_type

            if issubclass(expected_type, tuple) and hasattr(expected_type, '_fields'):
                result = await cursor.fetchone()
                result = expected_type(*result) if result else None
            elif hasattr(expected_type, '__origin__') and issubclass(expected_type.__origin__, Sequence):
                item_type = expected_type.__args__[0]
                if issubclass(item_type, tuple) and hasattr(item_type, '_fields'):
                    rows = await cursor.fetchall()
                    result = expected_type.__origin__(item_type(*item) for item in rows)
                else:
                    raise RecordNotFound("Invalid list item type specified")

            if result is None and not none_allowed:
                raise RecordNotFound
            return result

        return decorator

    return wrapper
