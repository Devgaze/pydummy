#!/usr/bin/python

# CONFIGURATION ==>
SOURCE_INDENTATION_LENGTH = 4
OUTPUT_INDENTATION_LENGTH = 4
SORT_KEYS_ON_OUTPUT = True
# <== CONFIGURATION ENDS

import sys, getopt, json

def to_bool(value):
    options = {
        'true': True,
        'True': True,
        'false': False,
        'False': False
    }
    return options.get(value, "To provide boolean value use one of the following: True, true, False, false")


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
                        node[label] = str(value)

                    elif value.lower() == 'bool' or value.lower() == 'boolean':
                        node[label] = to_bool('true')

                    elif value.startswith('ts'):
                        # value.lower() == 'ts' or value.lower() == 'timestamp':
                        node[label] = str(value)

                    else:
                        node[label] = 'You are trying to assign non-supported data type. Supported data types are: str, int, bool, ts.'

    return node
    

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["template=","jsonfile="])
    except getopt.GetoptError:
      print 'pydummy.py -i <templatefile> -o <jsonfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'pydummy.py -i <templatefile> -o <jsonfile>'
         sys.exit()
      elif opt in ("-i", "--template"):
         inputfile = arg
      elif opt in ("-o", "--jsonfile"):
         outputfile = arg

    x = parse_template(inputfile)
    with open(outputfile, 'wb') as outfile:
        json.dump(x, outfile, indent=OUTPUT_INDENTATION_LENGTH, sort_keys=SORT_KEYS_ON_OUTPUT)

if __name__ == '__main__': 
    main(sys.argv[1:])
