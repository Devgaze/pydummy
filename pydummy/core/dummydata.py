# -*- coding: utf-8 -*-
import random

class DummyData(object):

    def __init__(self):
        self.data = []

    def get_data(self):
        """Returns random name from the list"""
        i = self.get_random_data_element_index()
        return self.data[i]

    def get_random_data_element_index(self):
        return random.randint(0, len(self.data) -1)
