# -*- coding: utf-8 -*-
import sys
import os
import getopt
import json
import time
import random
from .strgen import PDStringGenerator

__version__ = "0.0.0"

# CONFIGURATION ==>
# ----------------------------------------
SOURCE_INDENTATION_LENGTH = 4
OUTPUT_INDENTATION_LENGTH = 4
SORT_KEYS_ON_OUTPUT = True

DATASOURCE_MAPPER = [
    ('name', 'DummyName'),
    ('surname', 'DummySurname'),
    ('address', 'DummyAddress'),
    ('company', 'DummyCompany'),
    ('street', 'DummyStreet'),
    ('city', 'DummyCity'),
    ('zip', 'DummyZip'),
    ('country', 'DummyCountry'),
]
# <== CONFIGURATION ENDS


def to_bool(value):
    options = {
        'true': True,
        'True': True,
        'false': False,
        'False': False
    }
    error_message = """
    To provide boolean value use one of the following: True, true, False, false
    """
    return options.get(value, error_message)


# nifty helper from
# http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def strTimeProp(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    # import pdb;pdb.set_trace()
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, "%Y-%m-%d %H:%M:%S", prop)


def get_random_integer():
    return random.randint(1, 999999)


def generate_number():
    return get_random_integer()


def generate_string():
    return PDStringGenerator()


def generate_boolean():
    return True if get_random_integer() % 2 == 0 else False


def generate_timestamp():
    start = "1990-01-01 00:00:00"
    end = "2019-12-31 23:59:59"
    return randomDate(start, end, random.random())


def parse_template(filepath, language, parent=None, from_line=0, indentation=0):
    if (filepath is None):
        print 'You didn\'t provide valid file path'
        return False

    node = parent if parent else {}

    with open(filepath) as f:
        for idx, line in enumerate(f):

            if idx >= from_line:
                leading_spaces = len(line) - len(line.lstrip())

                if leading_spaces == indentation:
                    prop, value = line.split(':')
                    label = prop.strip()
                    value = value.strip().lower()
                    print 'processing: %s' % line
                    if value.startswith('object'):
                        indent_by = leading_spaces + SOURCE_INDENTATION_LENGTH

                        if ('<' in value) or (' < ' in value):
                            value, repeater = value.split('<')
                            value.strip()
                            repeater.strip()
                            node[label] = []

                            for count in range(0, int(repeater)):
                                node[label].append(parse_template(
                                    filepath, language, None, idx + 1, indent_by
                                ))
                        else:
                            node[label] = {}
                            node[label] = parse_template(
                                filepath, language, node[label], idx + 1, indent_by
                            )

                    elif value == 'int' or value == 'integer':
                        node[label] = generate_number()

                    elif value == 'str' or value == 'string':
                        dep = [m for m in DATASOURCE_MAPPER if m[0] == label]
                        if len(dep) > 0:
                            strgen_obj = PDStringGenerator(
                                dep, label
                            )
                            node[label] = strgen_obj.output
                        elif label == 'email':
                            dependencies = [
                                ('domain', 'DummyDomain'),
                                ('name', 'DummyName'),
                                ('surname', 'DummySurname')
                            ]
                            strgen_obj = PDStringGenerator(dependencies, label)
                            node[label] = strgen_obj.output
                        else:
                            print "Encountered unmapped property: %s." % label
                            print "Assigning value `null`"
                            node[label] = None

                    elif value == 'bool' or value == 'boolean':
                        node[label] = generate_boolean()

                    elif value.split('=')[0] == 'ts' or value == 'timestamp':
                        node[label] = generate_timestamp()

                    else:
                        print """
                        You are trying to assign non-supported data type

                        %s
                            @line %d     %s

                        Supported data types are:
                        int|integer, str|string, bool|boolean, ts|timestamp
                        """ % (filepath, idx + 1, line)
                        sys.exit()

                elif leading_spaces < indentation:
                    break
    return node


def usage():
    os.system('clear')

    print """
    ***********
    * PyDummy *
    ***********

    Python command line tool for creation of dummy/fake/mocked data

    Parameters

        -i or --template    indicates a template (input) file
        -o or --jsonfile    indicates a JSON (output) file

    Usage

        # this call will default to `output.json` in current working directory
        python runner.py -i <template_filepath>
        python runner.py -i <template_filepath> -o <json_filename>
        python runner.py --template <filepath> --output <json_filename>

    If installed on system using `setup.py`

        pydummy -t <template_filepath> -o <json_filename>
        pydummy --template=<template_filepath> --output <json_filename>

    """


def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hi:o:",
            ["help", "template=", "jsonfile="])

    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--template"):
            inputfile = arg
        elif opt in ("-o", "--jsonfile"):
            outputfile = arg
        elif opt in ("-l", "--language"):
            language = arg
        else:
            print "unhandled option"
            usage()
            sys.exit()

    if not inputfile:
        usage()
        sys.exit()

    outputfile = outputfile if outputfile != "" else "output.json"
    language = language if language != "" else "en"
    cwd = os.getcwd()
    inputfile = os.path.join(cwd, inputfile)

    if not os.path.isfile(inputfile):
        # THIS IS LAME - fix this in next iteration
        print """
        File %s is not found.
        Template path should be relative to your current working directory.
        """ % inputfile
        sys.exit()

    outputfile = os.path.join(cwd, outputfile)

    parsed_template = parse_template(inputfile, language)

    with open(outputfile, 'wb') as outfile:
        json.dump(
            parsed_template, outfile,
            indent=OUTPUT_INDENTATION_LENGTH,
            sort_keys=SORT_KEYS_ON_OUTPUT
        )
