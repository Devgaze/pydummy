# -*- coding: utf-8 -*-
import sys
import os
import getopt
import json
from .datagen import DataGenerator


__version__ = "0.0.0"


def usage():
    os.system('clear')

    print """
    ***********
    * PyDummy *
    ***********

    Python command line tool for creation of dummy/fake/mocked data

    Parameters

        -h or --help        prints this help
        -i or --indent      set indentation spaces for JSON output
                            - default value is 4

        -j or --jsonfile    indicates a JSON (output) file
                            - default value is dummydata.json

        -l or --language    load dummy data for specific language
                            - default value is en

        -t or --template    indicates a template (input) file
        -s or --sort        indicates whether JSON keys should be sorted or not
                            - default value is yes

    Usage

        # loads data from template file my_template.txt and
        # creates dummy data in dumydata.json
        python runner.py -t my_template.txt

        # same as above but it will use indentation of 2 paces
        python runner.py -t my_templte.txt -i 2

        # same as above but it will put dummy data in my_dummy_data.json file
        python runner.py -t my_templte.txt -j my_dummy_data.json

        # same as first example but it will load Croatian values for dummy data
        python runner.py -t my_templte.txt -l hr

        # same as first example but it will disable auto sort of JSON keys
        python runner.py -t my_templte.txt -s no


    If installed on system using `pip install pydummy`

        pydummy -t <template_filepath> -o <json_filename>
        pydummy --template=<template_filepath> --output <json_filename>

    """


def main(argv):

    template = ''
    outputfile = ''
    language = ''
    indentation = 4
    sort_keys = True

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hi:j:l:t:s:",
            [
                "help",
                "indent=",
                "jsonfile=",
                "language=",
                "template=",
                "sort="
            ])

    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()

        elif opt in ("-t", "--template"):
            template = arg

        elif opt in ("-j", "--jsonfile"):
            outputfile = arg

        elif opt in ("-l", "--language"):
            language = arg

        elif opt in ("-i", "--indent"):
            indentation = int(arg)

        elif opt in ("-s", "--sort"):
            sort_keys = False if arg == 'no' else sort_keys

        else:
            print "unhandled option"
            usage()
            sys.exit()

    if not template:
        usage()
        sys.exit()

    else:
        cwd = os.getcwd()
        template = os.path.join(cwd, template)

        if not os.path.isfile(template):
            # THIS IS LAME - fix this in next iteration
            print """
            File %s is not found.
            Template path should be relative to your current working directory.
            """ % template
            sys.exit()

    language = language if language != "" else "en"

    outputfile = outputfile if outputfile != "" else "dummy.json"
    outputfile = os.path.join(cwd, outputfile)

    dg = DataGenerator(template, language)

    with open(outputfile, 'wb') as outfile:
        json.dump(
            dg.get(),
            outfile,
            indent=indentation,
            sort_keys=sort_keys
        )
