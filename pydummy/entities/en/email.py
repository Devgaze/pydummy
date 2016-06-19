# -*- coding: utf-8 -*-
from pydummy.core.dummydata import DummyData
from pydummy.eproxy import EntityProxy


class DummyEmail(DummyData):

    def __init__(self):
        pass

    def get_data(self):
        name = EntityProxy('name').get_instance().get_data()
        surname = EntityProxy('surname').get_instance().get_data()
        domain = EntityProxy('domain').get_instance().get_data()

        short_email = "%s@%s" % (name, domain)
        abbr_email = "%s%s@%s" % (name[0], surname, domain)
        abbr_email_with_dot = "%s.%s@%s" % (name[0], surname, domain)
        long_email = "%s.%s@%s" % (name, surname, domain)

        self.data = [
            short_email.lower(),
            abbr_email.lower(),
            abbr_email_with_dot.lower(),
            long_email.lower()
        ]

        # inherited method from DummyData class
        i = self.get_random_data_element_index()
        return self.data[i]
