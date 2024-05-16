#!/usr/bin/env python3
"""
    How to use redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
        Count how many store function called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            wrap the decorated function and return the wrapper
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            wrap the decorated function and return the wrapper
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    _redis = redis.Redis()
    fn = fn.__qualname__
    c = _redis.get(fn)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print(f"{fn} was called {c} times:")
    inputs = _redis.lrange(f"{fn}:inputs", 0, -1)
    outputs = _redis.lrange(f"{fn}:outputs", 0, -1)
    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print(f"{fn}(*{input}) -> {output}")


class Cache:
    '''
    Create A redis cache instance
        __init__ => create an instance of redis
        store    => cache data and return it's key
        get      => retrieve data by key
        get_str  => get a string
        get_int  => get a integer
    '''

    def __init__(self) -> None:
        """
            init redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            cache the data
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn:  Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
            Retrieve data by key
        """
        data = self._redis.get(key)
        if fn is not None:
            value = fn(data)
            return value
        return data

    def get_str(self, key: str) -> str:
        """
            Get Str by key
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
            Get Int by key
        """
        data = self._redis.get(key)
        try:
            value = int(data.decode("utf-8"))
        except Exception:
            value = 0
        return value
