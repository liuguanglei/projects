# -*- coding: utf-8 -*-

if __name__ == "__main__":
    import sys
    import json

    print len(sys.argv)
    if len(sys.argv) == 1:
        print "need argv"
    else:
        print sys.argv

    # print sys.argv[1]
    for i in sys.argv:
        print i