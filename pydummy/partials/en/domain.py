# -*- coding: utf-8 -*-

class DummyDomain:

    def __init__(self):
        self.domain_list = [
            'sweetmail.com',
            'fastsnail.net',
            'paperlessmail.org',
            'email.info',
            'academiamail.edu',
            'secretmail.gov',
            'notgmail.uk',
            'hayoo.us',
            'depost.de',
            'skandimail.dk'
        ]

        self.list_all()

    def list_all(self):
        return self.domain_list