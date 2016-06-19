# -*- coding: utf-8 -*-
from pydummy.core.dummydata import DummyData


class DummyCity(DummyData):

    def __init__(self):
        self.data = [
            'Vancouver',
            'New York',
            'Liverpool',
            'Dublin',
            'Perth',
            'Auckland',
            'London',
            'Miami',
            'Los Angeles',
            'Toronto',
        ]