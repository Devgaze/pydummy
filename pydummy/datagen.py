# -*- coding: utf-8 -*-
import os
from .eproxy import EntityProxy
from .etype import EntityType


class DataGenerator(object):
    """DataGenerator class"""

    def __init__(self, template, language='en'):
        """
        DataGenerator constructor
        - for arguments expects template file name or path
          and (optionaly) language
        """
        if template == '' or not self.is_file(template):
            raise "Invalid template file name or path"

        self.template = template
        self.language = language

        self.generate_data()

    def get(self):
        return self.data

    def is_file(self, template):
        return os.path.isfile(template)

    def generate_data(self):
        self.data = self.parse_template()

    def parse_template(self, lang='en', node={}, line_no=0, indent=0):
        """Reads the template file and calls appropriate entity class"""

        primitives = [
            'int', 'integer',
            'float',
            'bool', 'boolean',
            'ts', 'timestamp'
        ]

        with open(self.template) as f:
            for idx, line in enumerate(f):
                if idx >= line_no:
                    leading = len(line) - len(line.lstrip())

                    if leading < indent:
                        break

                    elif leading == indent:
                        prop, value = line.split(':', 1)
                        label = prop.strip()
                        value = value.strip().lower()

                        entity_type = EntityType(value)
                        entity = EntityProxy(label).getInstance()

                        typ = entity_type.get_type()

                        if typ == 'object':
                            start_from = idx + 1
                            lead_by = leading + 4

                            if entity_type.hasIterator():
                                node[label] = []

                                for count in entity_type.getIteratorRange():
                                    i = self.parse_template(
                                        lang, {}, start_from, lead_by
                                    )
                                    node[label].append(i)

                            else:
                                node[label] = {}
                                node[label] = self.parse_template(
                                    lang, node[label], start_from, lead_by
                                )

                        elif typ in primitives:
                            node[label] = entity_type.get_primitive_value()

                        else:
                            node[label] = entity.getData()

                    else:
                        pass

        return node
