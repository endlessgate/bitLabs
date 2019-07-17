from functools import wraps
from typing import TypeVar, Callable

T = TypeVar("T")


def change_returns_type(change_type: Callable[..., T]
                        ) -> Callable[..., Callable[..., T]]:
    def change(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return change_type(func(*args, **kwargs))
        return wrapper
    return change


to_dict = change_returns_type(dict)
to_tuple = change_returns_type(tuple)
to_list = change_returns_type(list)

