# -*- coding: utf-8 -*-
from pydummy.dummydata import DummyData


class DummyCompany(DummyData):

    def __init__(self):
        self.data = [
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