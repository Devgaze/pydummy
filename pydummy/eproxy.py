# -*- coding: utf-8 -*-
import importlib


class EntityProxy(object):
    """Auto-loader of entity classes based on provided type"""

    def __init__(self, identifier, lang='en'):
        if not identifier:
            raise "Cannot invoke entity loader without entity identifier"

        self.identifier = identifier
        self.language = lang

    def get_instance(self):
        """Tries to import module based on identifier and returns instance"""
        try:
            module = importlib.import_module(self.build_module_string())
            return getattr(module, self.build_class_name())()
        except ImportError:
            print "Trying to import %s.%s" % (
                self.build_module_string(),
                self.build_class_name()
            )
            print """
            This module doesn't exist. It may be you have added
            non-supported label in your template file.

            To fix it, in your current directory create following folder path

                pydummy/entities/en/%s.py

            Remember `en` can be any language you wish, for example `hr` for
            Croatian.

            Inside of that file paste following and update accordingly:

            # -*- coding: utf-8 -*-
            from pydummy.core.dummydata import DummyData


            class %s(DummyData):

                def __init__(self):
                    self.data = [
                        # your data list here
                    ]
            """ % (self.identifier, self.build_class_name())
            return None

    def build_module_string(self):
        """One word or multiple with dash"""
        module_name = self.identifier.lower()
        return "pydummy.entities.%s.%s" % (self.language, module_name)

    def build_class_name(self):
        """One word or multiple with dash"""
        return "Dummy%s" % self.identifier.capitalize()
