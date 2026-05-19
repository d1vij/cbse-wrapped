from functools import wraps
from typing import Any, Callable

type CacheKey = tuple[tuple[Any, ...], tuple[tuple[str, object], ...]]


# creates a tuple out of function args and kwargs
# since a tuple can be used as a key inside of a dict
def create_key(args: tuple[Any, ...], kwargs: dict[Any, Any]) -> CacheKey:
    return (args, tuple(sorted(kwargs.items())))


def memoize[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to memoize the return value of a function. Guarentees to return the same value for the same _*args_ and _**kwargs_ passed
    """
    cache: dict[CacheKey, R] = {}

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = create_key(args, kwargs)

        try:
            if key not in cache:
                cache[key] = fn(*args, **kwargs)
        except TypeError:  # args/kwargs has some unhashable type, eg pd.Series
            return fn(*args, **kwargs)

        return cache[key]

    return wrapper
