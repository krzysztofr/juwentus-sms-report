# -*- coding: utf-8 -*-


from settings import default as settings
try:
    from stop import dont_parse
except ImportError:
    dont_parse = False
from juwparser import parse, get_log, get_last_time

from importlib import import_module
import argparse


argparser = argparse.ArgumentParser(description="juwparser - parsing Juwentus logs")
argparser.add_argument('action', action='store', help="action (parse, getlog)", choices=('parse', 'getlog'))

action = argparser.parse_args().action

if action == 'parse':
    if dont_parse:
        print 'Parsing disabled with stop.dont_parse.'
    else:
        message_text = parse(html=get_log(settings=settings), last_time=get_last_time(), settings=settings)

        if message_text != '':
            sendermod = {}
            for sender in settings['SENDERS']:
                try:
                    sendermod[sender] = import_module('senders.%s' % sender)
                    sendermod[sender].send(message=message_text, settings=settings)
                except ImportError:
                    print 'No such sender: %s' % sender
elif action == 'getlog':
    print get_log(settings=settings)
