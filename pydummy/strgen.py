# -*- coding: utf-8 -*-

"""pydummy.strgen: String Generator class generates different string entities"""
import os, sys, importlib
from random import randint
from .partials.domain import DummyDomain

class PDStringGenerator:

    def __init__(self, modules_to_load, identifier, locale='en'):
        self.modules_to_load = modules_to_load
        self.locale = locale
        self.modules = {}

        # fetch data
        self.output = self.generate_by_identifier(identifier)

        # if self.identifier == 'email' or self.identifier == 'mail':
        #     self.output = self.generate_email()
        # elif self.identifier == '':
        #     self.output = 'dummy data'
        # else:
        #     self.output = self.generate_by_identifier()


    def load_data_sources(self):
        
        for module in self.modules_to_load:
            module_path = "pydummy.partials.%s.%s.%s" % (self.locale, module[0], module[1])
            
            # check for file existance
            if self.test_module_path(module_path):
                self.load_module(module_path, module[0])
            else:
                print "Modules \n %s \n doesn't exist. Exiting the application." % (module_path)
                sys.exit()


    def load_module(self, mod, identifier):
        # print "Loading: %s" % mod
        fragments = mod.split(".")
        path = ".".join(fragments[:-1])
        cls = fragments[-1]
        module = importlib.import_module(path)
        cls = getattr(module, cls)()
        self.modules[identifier] = cls


    def test_module_path(self, mod):
        fragments = mod.split('.')[:-1]
        fragments = os.path.join(*fragments)
        path = os.path.join(os.getcwd(), fragments+'.py')
        return os.path.isfile(path)


    def get_random_element(self, data):
        random_index = randint(0, len(data) - 1)
        return data[random_index]

    def generate_by_identifier(self, identifier):
        if identifier == 'email' or identifier == 'mail':
            return self.generate_email()
        else:
            # load modules
            self.load_data_sources()
            return self.get_random_element(self.modules[identifier].list_all())
        
    def generate_email(self):
        self.load_data_sources()
        # import pdb;pdb.set_trace()
        email_name = self.get_random_element(self.modules['name'].list_all())
        email_surname = self.get_random_element(self.modules['surname'].list_all())
        email_domain = self.get_random_element(self.modules['domain'].list_all())
        
        short_email = "%s@%s" % (email_name, email_domain)
        abbr_email = "%s%s@%s" % (email_name[0], email_surname, email_domain)
        abbr_email_with_dot = "%s.%s@%s" % (email_name[0], email_surname, email_domain)
        long_email = "%s.%s@%s" % (email_name, email_surname, email_domain)

        return self.get_random_element([short_email, abbr_email, abbr_email_with_dot, long_email])




