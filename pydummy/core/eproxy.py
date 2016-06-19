# -*- coding: utf-8 -*-
import importlib

IMPORT_ERROR_MESSAGE = """
Trying to import: %s.%s

This module doesn't exist. It may be you have added
non-supported label in your template file.

To fix it, in your current directory create following folder path

    dummyentities/%s/%s.py

Remember `%s` can be any language you wish, for example `hr` for
Croatian.

Inside of that file paste following and update accordingly:

# -*- coding: utf-8 -*-
from pydummy.core.dummydata import DummyData


class %s(DummyData):

    def __init__(self):
        self.data = [
            # your data list here
        ]
"""


class EntityProxy(object):
    """Auto-loader of entity classes based on provided type"""

    def __init__(self, identifier=None, lang='en'):
        if not identifier:
            raise "Cannot invoke entity loader without entity identifier"

        self.identifier = identifier
        self.language = lang

    def get_instance(self):
        """Tries to import module based on identifier and returns instance"""
        try:
            module = importlib.import_module(self.package_module_string())
            return getattr(module, self.build_class_name())()
        except ImportError:
            try:
                module = importlib.import_module(self.local_module_string())
                return getattr(module, self.build_class_name())()
            except ImportError:
                return self.load_import_error_help()

    def package_module_string(self):
        """One word or multiple with dash"""
        module_name = self.identifier.lower()
        return "pydummy.entities.%s.%s" % (self.language, module_name)

    def local_module_string(self):
        """One word or multiple with dash"""
        module_name = self.identifier.lower()
        return "dummyentities.%s.%s" % (self.language, module_name)

    def build_class_name(self):
        """One word or multiple with dash"""
        return "Dummy%s" % self.identifier.capitalize()

    def load_import_error_help(self):
        """Helper function to display import error and fix"""
        print IMPORT_ERROR_MESSAGE % (
            self.identifier,
            self.build_class_name(),
            self.language,
            self.package_module_string(),
            self.language,
            self.build_class_name()
        )
        return None
