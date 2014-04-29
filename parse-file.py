# -*- coding: utf-8 -*-

# to run:
# python parse-file.py filename [last-time]

import sys
import datetime

from settings import default as settings

from juwparser import parse

filename = sys.argv[1]
try:
    last_time = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M:%S')
except ValueError:
    print 'Invalid time provided: ' + sys.argv[2] + '. Use "%Y-%m-%d %H:%M:%S" format.'
    sys.exit()
except IndexError:
    last_time = datetime.datetime.strptime('2014-04-21 00:00:00', '%Y-%m-%d %H:%M:%S')

try:
    with open(sys.argv[1], 'r') as l:
        log = l.read()
    print parse(html=log, last_time=last_time, settings=settings)
except IOError:
    print 'No such file: ' + sys.argv[1]

