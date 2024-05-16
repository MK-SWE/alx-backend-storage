#!/usr/bin/env python3
"""
    How to use redis
"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    '''Create A redis cache instance'''
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
