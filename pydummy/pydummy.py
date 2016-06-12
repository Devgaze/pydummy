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

def generate_dummy_content(identifier):
    print identifier


def parse_template(filepath, parent_node = None, parse_from_line = 0, indentation = 0):
    if (filepath is None):
        print 'You didn\'t provide valid file path'
        return False

    output = []
    id_counter = 0
    node = parent_node if parent_node else {};
    
    with open(filepath) as f:
        for idx, line in enumerate(f):
            if idx >= parse_from_line:
                leading_spaces = len(line) - len(line.lstrip())

                if leading_spaces == indentation:
                    
                    prop, value = line.split(':')
                    label = prop.strip()
                    value = value.strip()

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

                    
                    elif value.lower() == 'int' or value.lower() == 'integer':
                        node[label] = ++id_counter

                    elif value.lower() == 'str' or value.lower() == 'string':
                        node[label] = generate_dummy_content(label)

                    elif value.lower() == 'bool' or value.lower() == 'boolean':
                        node[label] = to_bool('true')

                    elif value.startswith('ts'):
                        # value.lower() == 'ts' or value.lower() == 'timestamp':
                        node[label] = str(value)

                    else:
                        node[label] = 'You are trying to assign non-supported data type. Supported data types are: str, int, bool, ts.'

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

