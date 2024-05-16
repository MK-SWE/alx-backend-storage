#!/usr/bin/env python3
"""
    How to use redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional



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
        if fn != None:
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
