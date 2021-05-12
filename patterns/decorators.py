from time import time
from functools import wraps


def timer(name):
    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            before = time()
            result = func(*args, **kwargs)
            after = time()
            print(f'[DEBUG] -- Elapsed time for {name} is: {after - before:2.2f} ms')
            return result
        return wrapper
    return inner_function


def app_route(routes: dict, url: str):
    def inner_function(cls):
        routes[url] = cls()
        return routes
    return inner_function



