# -*- coding: utf-8 -*-

class DummyStreet:

    def __init__(self):
        self.street_list = [
            '71 East Hastings',
            '72 East Hastings',
            '713 East Hastings',
            '74 East Hastings',
            '75 East Hastings',
            '76 East Hastings',
            '77 East Hastings',
            '78 East Hastings',
            '784 East Hastings',
            '799 East Hastings'
        ]

        self.list_all()

    def list_all(self):
        return self.street_list