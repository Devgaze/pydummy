# -*- coding: utf-8 -*-

class DummySurname:

    def __init__(self):
        self.surname_list = [
            'Seth',
            'McDonell',
            'Richards',
            'Smith',
            'Albright',
            'Mackenzie',
            'Grant',
            'Haggard',
            'Abbott',
            'Crawford'
        ]
        
        self.list_all()

    def list_all(self):
        return self.surname_list