import functools
import inspect

from django.db import close_old_connections


def recycle_db_connections(func):
    """Closes stale/broken db connections before and after a scheduled job.

    Django recycles connections from the request signals, which never fire in
    the user bot process, so a connection dropped by the server stays cached
    and every later query fails with `InterfaceError: connection already closed`.
    """
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            close_old_connections()
            try:
                return await func(*args, **kwargs)
            finally:
                close_old_connections()

        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        close_old_connections()
        try:
            return func(*args, **kwargs)
        finally:
            close_old_connections()

    return wrapper
