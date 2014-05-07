# -*- coding: utf-8 -*-

from time import strftime


def send(message, settings):
    print "\n".join(("[%s] " % strftime("%Y-%m-%d %H:%M:%S") + s for s in message.split("\n")))