# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import datetime
import pycurl
import cStringIO
import re


def get_last_time(last_time_filename="lasttime.txt"):
    """Gets the time when last event occured.
    """

    # check last time log
    try:
        lt_file = open(last_time_filename, 'r')
        last_time = datetime.datetime.strptime(lt_file.read().strip(), '%Y-%m-%d %H:%M:%S')
        lt_file.close()
    except IOError:
        last_time = datetime.datetime.now() - datetime.timedelta(days=1)

    return last_time


def get_log(settings):
    """Gets log in HTML form from Juwentus website.
    """
    # log in
    c = pycurl.Curl()
    c.setopt(c.COOKIEFILE, '')
    c.setopt(c.POST, 1)
    c.setopt(c.URL, 'https://ochrona.juwentus.pl/index.php')
    c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36')
    c.setopt(c.POSTFIELDS, 'logon=1&login=%s&haslo=%s' % (settings['JUWENTUS_LOGIN'], settings['JUWENTUS_PASS']))
    c.perform()

    buf = cStringIO.StringIO()

    # download log from last day
    c.setopt(c.URL, 'https://ochrona.juwentus.pl/sources/sygnaly_on_line_rap.php?wyswietl=1&okr=1&idobiektu=%s' % settings['JUWENTUS_OBJECT_ID'])
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()

    result = buf.getvalue()
    buf.close()

    return result


def parse(html, last_time, settings, last_time_filename='lasttime.txt'):
    """Parses HTML code, returns message.
    """


    soup = BeautifulSoup(html)

    message = {}
    users_zal = []
    users_wyl = []

    first = True

    # parse table
    for tr in soup.find_all('tr'):
        items = tr.find_all('td')
        # skip first row
        if items[0].string == 'Data':
            continue

        time = items[0].string + ' ' + items[1].string
        signal = items[2].string
        desc = items[3].string
        if items[5].string is None:
            continue  # "Linia 0" - empty zone_no
        zone_no = int(items[5].string)
        zone_desc = unicode(items[6].string)
        try:
            line_id = int(re.search('Linia (\d+)', desc).group(1))
        except AttributeError:
            line_id = None

        if line_id is not None:
            try:
                line_name = settings['LINES'][line_id]
            except KeyError:
                line_name = str(line_id)

        try:
            user_id = int(re.search('ytk\.(\d+)', desc).group(1))
        except AttributeError:  # jezeli nie da sie ustalic uzytkownika
            user_id = None

        if user_id in settings['IGNORE_USERS']:
            continue

        if user_id is not None:
            try:
                user_name = settings['USERS'][user_id]
            except KeyError:
                user_name = 'u' + str(user_id)

        time_diff = (datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') - last_time)

        if time_diff <= datetime.timedelta(seconds=0):
            # cut here
            break
        if first:
            lt_file = open(last_time_filename, 'w')
            lt_file.write(time)
            lt_file.close()
            first = False

        if signal == u'ZAŁĄCZENIE' and 'zal' not in settings['IGNORE_ACTIONS']:
            if message.get('zal') is None:
                message['zal'] = []
            message['zal'].append(settings['ZONES'][zone_no])
            if user_name not in users_zal:
                users_zal.append(user_name)
        if signal == u'WYŁĄCZENIE' and 'wyl' not in settings['IGNORE_ACTIONS']:
            if message.get('wyl') is None:
                message['wyl'] = []
            message['wyl'].append(settings['ZONES'][zone_no])
            if user_name not in users_wyl:
                users_wyl.append(user_name)
        if signal == u'KOMUNIKAT' and 'kom' not in settings['IGNORE_ACTIONS']:
            if message.get('kom') is None:
                message['kom'] = []
            message['kom'].append(settings['ZONES'][zone_no])
        if signal == u'WŁAMANIE' and 'wlam' not in settings['IGNORE_ACTIONS']:
            if message.get('wlam') is None:
                message['wlam'] = []
            message['wlam'].append(settings['ZONES'][zone_no] + " (" + line_name + ")")
        if signal == u'NAPAD' and 'napad' not in settings['IGNORE_ACTIONS']:
            message['napad'] = True  # specjalny przypadek, tutaj tylko fakt napadu, bez strefy

    message_text = ''

    if message.get('zal') is not None:
        if message_text != '':
            message_text += "\n"
        message_text += "ZALACZONO (" + ', '.join(users_zal) + "): " + ', '.join(message['zal'])
    if message.get('wyl') is not None:
        if message_text != '':
            message_text += "\n"
        message_text += "WYLACZONO (" + ', '.join(users_wyl) + "): " + ', '.join(message['wyl'])
    if message.get('kom') is not None:
        if message_text != '':
            message_text += "\n"
        message_text += "KOMUNIKAT: " + ', '.join(message['kom'])
    if message.get('wlam') is not None:
        if message_text != '':
            message_text += "\n"
        message_text += "WLAMANIE: " + ', '.join(message['wlam'])
    if message.get('napad') is not None:
        if message_text != '':
            message_text += "\n"
        message_text += "NAPAD!"

    return message_text