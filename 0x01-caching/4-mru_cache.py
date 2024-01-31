#!/usr/bin/env python3
"""MRU Caching."""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache inherits from BaseCaching"""
    def __init__(self):
        """Init cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def get(self, key):
        """Retrieves item by key.
        """
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)

    def put(self, key, item):
        """Adds an item to cache.
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                mru_key, _ = self.cache_data.popitem(False)
                print("DISCARD:", mru_key)
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)
        else:
            self.cache_data[key] = item
