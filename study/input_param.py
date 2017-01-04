# -*- coding: utf-8 -*-

import sys, getopt
import base64

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")

input_file = ""
output_file = ""

for op, value in opts:
    if op == "-i":
        input_file = value
        print input_file
    elif op == "-o":
        value = base64.b64decode(value)
        output_file = value
        print output_file
    elif op == "-h":
        # usage()
        sys.exit()
