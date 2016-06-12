# -*- coding: utf-8 -*-


"""pydummy.pydummy: provides entry point main()."""


__version__ = "0.0.0"

# from .stuff import Stuff


# CONFIGURATION ==>
SOURCE_INDENTATION_LENGTH = 4
OUTPUT_INDENTATION_LENGTH = 4
SORT_KEYS_ON_OUTPUT = True
# <== CONFIGURATION ENDS

import sys, os, getopt, json

# class DummyContent:

#     def __init__(self, content_identifier):
#         self.identifier = content_identifier

def to_bool(value):
    options = {
        'true': True,
        'True': True,
        'false': False,
        'False': False
    }
    return options.get(value, "To provide boolean value use one of the following: True, true, False, false")


def generate_number():
    return 1234
    
def generate_string():
    return 'heyaaa'
    
def generate_boolean():
    return True
    
def generate_timestamp():
    return '2016-06-16T15:03:12.000Z'
    

def parse_template(filepath, parent_node = None, parse_from_line = 0, indentation = 0):
    if (filepath is None):
        print 'You didn\'t provide valid file path'
        return False

    output = []
    id_counter = 0
    node = parent_node if parent_node else {};    

    with open(filepath) as f:
        for idx, line in enumerate(f):
            line_metadata = {}
            if idx >= parse_from_line:
                leading_spaces = len(line) - len(line.lstrip())

                if leading_spaces == indentation:
                    
                    prop, value = line.split(':')
                    label = prop.strip()
                    value = value.strip().lower()

                    if value.startswith('object'):
                        if  ('<' in value) or (' < ' in value):
                            value, repeater = value.split('<')
                            value.strip()
                            repeater.strip()
                            node[label] = []
                            
                            for count in range(0, int(repeater)):
                                node[label].append(parse_template(filepath, None, idx + 1, leading_spaces + SOURCE_INDENTATION_LENGTH))
                        else:
                            node[label] = {}
                            node[label] = parse_template(filepath, node[label], idx + 1, leading_spaces + SOURCE_INDENTATION_LENGTH)

                    
                    elif value == 'int' or value == 'integer':
                        node[label] = generate_number()

                    elif value == 'str' or value == 'string':
                        node[label] = generate_string()

                    elif value == 'bool' or value == 'boolean':
                        node[label] = generate_boolean()

                    elif value.split('=')[0] == 'ts' or value == 'timestamp':
                        node[label] = generate_timestamp()

                    else:
                        print """
                        You are trying to assign non-supported data type found in 

                        %s
                            @line %d     %s

                        Supported data types are: int|integer, str|string, bool|boolean, ts|timestamp 
                        """ % (filepath, idx + 1, line)
                        sys.exit()

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

        python runner.py -i <template_filepath> -o <json_filename>
        python runner.py --template <template_filepath> --output <json_filename>

    If installed on system using `setup.py` 

        pydummy -t <template_filepath> -o <json_filename>
        pydummy --template=<template_filepath> --output <json_filename>

    """

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "template=", "jsonfile="])
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
        else:
            print "unhandled option"
            usage()
            sys.exit()

    if not inputfile or not outputfile:
        usage()
        sys.exit()
  
    cwd = os.getcwd()
    inputfile = os.path.join(cwd, inputfile)
    
    if not os.path.isfile(inputfile):
        # THIS IS LAME - fix this in next iteration
        print "File %s is not found. Provide file path to your template relative to your current working directory." % template_abs_path
        sys.exit()
    
    outputfile = os.path.join(cwd, outputfile)

    parsed_template = parse_template(inputfile)
    
    with open(outputfile, 'wb') as outfile:
        json.dump(parsed_template, outfile, indent=OUTPUT_INDENTATION_LENGTH, sort_keys=SORT_KEYS_ON_OUTPUT)

