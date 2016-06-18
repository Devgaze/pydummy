# -*- coding: utf-8 -*-
import re
import time
import random
import datetime


class EntityType(object):
    """Entity type handler"""

    def __init__(self, identifier):
        if not identifier:
            raise "Cannot invoke type loader without type identifier"

        self.identifier = identifier
        self.DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

        if '<' in self.identifier:
            self.typ, self.modifier = self.identifier.split('<', 1)

        elif '=' in self.identifier:
            self.typ, self.modifier = self.identifier.split('=', 1)

        else:
            self.typ = self.identifier
            self.modifier = None

    def hasIterator(self):
        """Check whether type object should be represented as object or list"""
        return True if '<' in self.identifier else False

    def getIteratorRange(self):
        """Returns number of iterations to be performed on object"""
        top = int(self.identifier.split('<', 1)[1].strip())
        return range(0, top)

    def get_type(self):
        """Returns defined type"""
        return self.typ.strip()

    def get_modifier(self):
        """Returns defined modifiers of a type"""
        return self.modifier

    def get_primitive_value(self):
        """
        Calls different functions for generating random primitive values
        based on given entity type.
        """
        if self.typ == 'int' or self.typ == 'integer':
            x = self.get_integer()
            return x

        elif self.typ == 'float':
            return self.get_float()

        elif self.typ == 'bool' or self.typ == 'boolean':
            return self.get_bool()

        elif self.typ == 'ts' or self.typ == 'timestamp':
            return self.get_timestamp()

        else:
            return ""

    def get_integer(self):
        """
        Generates random integer in either default or user defined range.
        """
        if self.modifier:
            regex = '^\[[+-]?\d+\:[+-]?\d+\]$'
            modifier_validator = re.match(regex, self.modifier)

            if modifier_validator:
                self.modifier = self.modifier.strip('[').strip(']')
                start, end = self.modifier.split(':')
                start = int(start)
                end = int(end)

                if start < end:
                    return random.randint(start, end)

                else:
                    print "Error at: %s " % self.identifier
                    print "For integer modifiers use following format:"
                    print "Example:  houseNumber:int=[1:126]"
                    print "Falling back to app-range random integer"
                    return random.randint(0, 999999)

            else:
                print """
                Modifier found in %s, but format is not correct.
                """ % self.identifier
                print "For integer modifiers use following format:"
                print "Example:  houseNumber:int=[1:126]"
                print "Falling back to app-range random integer"
                return random.randint(0, 999999)

        else:
            return random.randint(0, 999999)

    def get_float(self):
        """
        Generates random float in either default or user defined range.
        Supports additional modifier for legth of decimal places.
        """
        if self.modifier:
            regex = '^\[[+-]?\d+\.\d+\:[+-]?\d+\.\d+\](%\d+)?$'
            modifier_validator = re.match(regex, self.modifier)

            if modifier_validator:
                if '%' in self.modifier:
                    rng, l = self.modifier.split('%')
                    l = l if l <= 17 and l >= 1 else 17

                else:
                    rng = self.modifier
                    l = 2

                start, end = rng.strip('[').strip(']').split(':')
                start = float(start)
                end = float(end)

                if start < end:
                    return round(random.uniform(start, end), l)

                else:
                    print "Error at: %s " % self.identifier
                    print "For float modifiers use following format:"
                    print "Example:  houseNumber:float=[122.33:126.21]"
                    print "Falling back to app-range random float"
                    return round(random.uniform(0, 999999), l)

            else:
                print """
                Modifier found in %s, but format is not correct.
                """ % self.identifier
                print "For float modifiers use following format:"
                print "Example:  houseNumber:float=[122.33:126.21]"
                print "Falling back to app-range random float"
                return round(random.uniform(0, 999999), 2)

        else:
            return round(random.uniform(0, 999999), 2)

    def get_bool(self):
        """Returns True or False based on random integer"""
        return True if self.get_random_integer() % 2 == 0 else False

    def get_random_integer(self):
        """Helper function to get random integer"""
        return random.randint(1, 999999)

    def get_random(self):
        """Helper function to get random integer"""
        return random.random()

    def get_timestamp(self):
        """
        Generates random float in either default or user defined range.
        Supports additional modifier for legth of decimal places.
        """
        if self.modifier:
            regex = (
                '^\['
                '\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}'
                '\|'
                '\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}'
                '\]'
                '(%(Z|[+-][1-9][1-2]?))?$'
            )

            modifier_validator = re.match(regex, self.modifier, re.IGNORECASE)

            if modifier_validator:
                if '%' in self.modifier:
                    rng, tz = self.modifier.split('%')

                else:
                    rng = self.modifier
                    tz = 'Z'

                start, end = rng.strip('[').strip(']').split('|')
                dt_format = self.DATETIME_FORMAT

                if self.check_date_order(start, end):
                    prop = self.get_random()
                    dt = self.strTimeProp(start, end, dt_format, prop)
                    return self.to_iso_datetime_format(dt, tz)

                else:
                    print """
                    Error at: %s

                    For timestamp modifiers use following format:
                    published:ts=[2016-01-01T00:00:00|2016-12-31T23:59:59]

                    optionaly with timezone
                    Zulu or UTC
                    published:ts=[2016-01-01T00:00:00|2016-12-31T23:59:59]\%Z

                    or in hours with prefix (+/-)
                    published:ts=[2016-01-01T00:00:00|2016-12-31T23:59:59]+11

                    Falling back to app-range random timestamp"
                    """ % self.identifier
                    dt = self.get_app_date_range()
                    return self.to_iso_datetime_format(dt, tz)

            else:
                print """
                Modifier found in %s, but format is not correct.
                """ % self.identifier
                print "For integer modifiers use following format:"
                print "Example:  houseNumber:int=[1:126]"
                print "Falling back to app-range random integer"
                dt = self.get_app_date_range()
                return self.to_iso_datetime_format(dt)

        else:
            dt = self.get_app_date_range()
            return self.to_iso_datetime_format(dt)

    # nifty helper from
    # http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    def strTimeProp(self, start, end, time_format, prop):
        """
        Helper function for EntityType.get_timestamp() method.
        It takes 2 parameters in format of datetime which will be used as
        a range.

        Returns string representation of random datetime from given range.
        """
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(time_format, time.localtime(ptime))

    def to_iso_datetime_format(self, dt, tz=None):
        """
        Helper function for EntityType.get_timestamp() method.
        It takes 2 parameters datetime representation and timezone.
        After processing it will return ISO 8601 string representation
        of date with accompanying timezone.
        """
        if tz == 'Z':
            return "%s%s" % (dt, tz)

        elif not tz:
            return dt

        else:
            diff = int(tz[1:])
            diff = str(diff) if diff >= 10 else "0%d" % diff
            prefix = tz[0]

            return "%s%s%s:00" % (dt, prefix, diff)

    def check_date_order(self, start, end):
        """
        Helper function for EntityType.get_timestamp() method.
        It takes 2 parameters, representations of datetime and then it
        checks whether the start date is smaller than end date and
        accordingly returns True or False.
        """
        start = datetime.datetime.strptime(start, self.DATETIME_FORMAT)
        end = datetime.datetime.strptime(end, self.DATETIME_FORMAT)

        return start < end

    def get_app_date_range(self):
        """
        Helper function for EntityType.get_timestamp() method.
        It returns list of 2 values, string representations of datetime object.
        """
        dt_format = self.DATETIME_FORMAT

        two_years_from_now = datetime.timedelta(days=2 * 365)

        start = datetime.datetime.now() - two_years_from_now
        start = start.strftime(dt_format)

        end = datetime.datetime.now() + two_years_from_now
        end = end.strftime(dt_format)

        prop = self.get_random()

        return self.strTimeProp(start, end, dt_format, prop)
