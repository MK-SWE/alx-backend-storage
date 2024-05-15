#!/usr/bin/env python3
"""
  function that inserts a new document in a collection based on kwargs:
"""
import pymongo


def insert_school(mongo_collection, **kwargs) -> int :
    """
        return the id of new inserted
    """
    return mongo_collection.insert(kwargs)
