# -*- coding: utf-8 -*-

class DummyCompany:

    def __init__(self):
        self.company_list = [
            ('Maxwell Inc.', 'maxwell.com'),
            ('Rickman & Son', 'rickmanandson.us'),
            ('Marshall Transports Ltd.', 'marshall.co.uk'),
            ('O\'Briens Brewery', 'brewitup.ie'),
            ('DownUnder', 'downunder.au'),
            ('Simmons Guns', 'simmonsguns.us'),
            ('Trapple Rentals', 'trapple.ie'),
            ('Happy Ham', 'happyham.com'),
            ('Misfit Inc.', 'misfit.co.nz'),
            ('Tropical Jet Airlines', 'tropicaljet.us')
        ]
        
        self.list_all()

    def list_all(self):
        return self.company_list