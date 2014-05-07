# -*- coding: utf-8 -*-

from time import strftime

def send(message, settings):
    with open(settings['FILE_SAVE'], 'a') as logfile:
        logfile.write("\n".join(("[%s] " % strftime("%Y-%m-%d %H:%M:%S") + s for s in message.split("\n"))))
        logfile.write("\n")
