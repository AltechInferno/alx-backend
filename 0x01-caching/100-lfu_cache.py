#!/usr/bin/env python3
"""Least Frequently Used caching module.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """an object that allows storing and
    retrieving of items from a dictionary with a LFU
    removal method when limit is reached
    """
    def __init__(self):
        """Init cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.keys_freq = []

    def __reorder_items(self, mru_key):
        """Rearranges items in cache based on the most
        recently used item.
        """
        freq = 0
        max_positions = []
        pos = 0
        ins_pos = 0
        for i, key_freq in enumerate(self.keys_freq):
            if key_freq[0] == mru_key:
                freq = key_freq[1] + 1
                pos = i
                break
            elif len(max_positions) == 0:
                max_positions.append(i)
            elif key_freq[1] < self.keys_freq[max_positions[-1]][1]:
                max_positions.append(i)
        max_positions.reverse()
        for p in max_positions:
            if self.keys_freq[p][1] > freq:
                break
            ins_pos = p
        self.keys_freq.pop(pos)
        self.keys_freq.insert(ins_pos, [mru_key, freq])

    def get(self, key):
        """Retrieves item by key.
        """
        if key is not None and key in self.cache_data:
            self.__reorder_items(key)
        return self.cache_data.get(key, None)

    def put(self, key, item):
        """Adds an item to cache.
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                lfu_key, _ = self.keys_freq[-1]
                self.cache_data.pop(lfu_key)
                self.keys_freq.pop()
                print("DISCARD:", lfu_key)
            self.cache_data[key] = item
            ins = len(self.keys_freq)
            for j, key_freq in enumerate(self.keys_freq):
                if key_freq[1] == 0:
                    ins = j
                    break
            self.keys_freq.insert(ins, [key, 0])
        else:
            self.cache_data[key] = item
            self.__reorder_items(key)
