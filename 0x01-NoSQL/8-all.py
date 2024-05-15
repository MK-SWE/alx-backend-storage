#!/usr/bin/env python3
"""
  List all items in mongodb database
"""
import pymongo
from typing import List


def list_all(mongo_collection) -> list:
    """
        return list
    """
    if(not mongo_collection):
        return []
    results = mongo_collection.find()
    return [result for result in results]
