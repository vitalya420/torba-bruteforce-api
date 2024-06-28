import inspect
import os
import types
from functools import wraps
from typing import get_type_hints, Union, Sequence, Optional

from app.database.abc import Executor
from app.database.exceptions import RecordNotFound


def load_sql_file(file):
    abs_path = os.path.join(os.getcwd(), file)
    with open(abs_path, 'r') as query_file_:
        return query_file_.read()


class Query:
    def __init__(self):
        self._name_func_map = {}

    def get_sql_query(self, name, __default=None):
        return self._name_func_map.get(name, __default)

    @staticmethod
    async def _inside_decorator(sql_query, func, cursor_callback, *args, **kwargs):
        executor_instance = args[0]
        if not isinstance(executor_instance, Executor):
            raise RuntimeError('Fuck this this, I\'m out')
        session = executor_instance.session

        sig = inspect.signature(func)

        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        params = bound_args.arguments

        params.pop('self', None)

        cursor = await session.execute(sql_query, params)
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

    def file(self, path: str, name: Optional[str] = None, cursor_callback=None):
        def wrapper(func):
            sql_query = load_sql_file(path)
            self._name_func_map[name or func.__name__] = sql_query

            @wraps(func)
            async def decorator(*args, **kwargs):
                return await self._inside_decorator(sql_query, func, cursor_callback, *args, **kwargs)

            return decorator

        return wrapper

    def __call__(self,
                 sql_query: str,
                 name: Optional[str] = None,
                 cursor_callback=None):

        def wrapper(func):
            self._name_func_map[name or func.__name__] = sql_query

            @wraps(func)
            async def decorator(*args, **kwargs):
                return await self._inside_decorator(sql_query, func, cursor_callback, *args, **kwargs)

            return decorator

        return wrapper


query = Query()
