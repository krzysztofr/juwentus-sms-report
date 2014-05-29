# -*- coding: utf-8 -*-

from juwparser import timestampize


def send(message, settings):
    with open(settings['FILE_SAVE'], 'a') as logfile:
        logfile.write(timestampize(message))
        logfile.write("\n")
