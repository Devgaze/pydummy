# -*- coding: utf-8 -*-

class DummyCity:

    def __init__(self):
        self.city_list = [
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

        self.list_all()

    def list_all(self):
        return self.city_list