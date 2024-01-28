#!/usr/bin/env python3
"""Hypermedia pagination
"""
import csv
import math
from typing import Dict, List, Tuple

def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """gets index range from a given page and page size.
    """

    return ((page - 1) * page_size, ((page - 1) * page_size) + page_size)


class Server:
    """class to paginate a db of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None


    def dataset(self) -> List[List]:
        """Our cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as df:
                reader = csv.reader(df)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """gets a page of data.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        p_data = self.dataset()
        if start > len(p_data):
            return []
        return p_data[start:end]


    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """gathers information about a page.
        """
        p_data = self.get_page(page, page_size)
        start, end = index_range(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)
        return {
            'page_size': len(data),
            'page': page,
            'data': p_data,
            'next_page': page + 1 if end < len(self.__dataset) else None,
            'prev_page': page - 1 if start > 0 else None,
            'total_pages': total_pages
        }
