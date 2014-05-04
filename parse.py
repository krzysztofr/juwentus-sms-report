# -*- coding: utf-8 -*-


from settings import default as settings

from juwparser import parse, get_log, get_last_time

from importlib import import_module


def main():

    message_text = parse(html=get_log(settings=settings), last_time=get_last_time(), settings=settings)

    if message_text != '':
        sendermod = {}
        for sender in settings['SENDERS']:
            sendermod[sender] = import_module('senders.%s' % sender)
            sendermod[sender].send(message=message_text, settings=settings)

if __name__ == "__main__":
    main()