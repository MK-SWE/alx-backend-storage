#!/usr/bin/env python3
"""
  function that inserts a new document in a collection based on kwargs:
"""
import pymongo


def insert_school(mongo_collection, **kwargs) -> int | None:
    """
        return the id of new inserted
    """
    if(not mongo_collection):
        return None
    return mongo_collection.insert(kwargs)
