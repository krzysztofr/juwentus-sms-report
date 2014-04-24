# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime
from smsapi.client import SmsAPI
from smsapi.responses import ApiError

import pycurl, cStringIO
import settings

try:
    DEBUG = settings.DEBUG
except NameError:
    DEBUG = False



# log in
c = pycurl.Curl()
c.setopt(c.COOKIEFILE, '')
c.setopt(c.POST, 1)
c.setopt(c.URL, 'https://ochrona.juwentus.pl/index.php')
c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36')
c.setopt(c.POSTFIELDS, 'logon=1&login=%s&haslo=%s' % (settings.JUWENTUS_LOGIN, settings.JUWENTUS_PASS))
c.perform()


buf = cStringIO.StringIO()


# download log from last day
c.setopt(c.URL, 'https://ochrona.juwentus.pl/sources/sygnaly_on_line_rap.php?wyswietl=1&okr=1&idobiektu=%s' % (settings.JUWENTUS_OBJECT_ID))
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()


result = buf.getvalue()
buf.close()

# check last time log
try:
    lt_file = open('lasttime.txt', 'r')
    last_time = datetime.datetime.strptime(lt_file.read().strip(), '%Y-%m-%d %H:%M:%S') 
    lt_file.close()
except IOError:
    last_time = datetime.datetime.now() - datetime.timedelta(days=1)


soup = BeautifulSoup(result)

message = {}

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

    time_diff = (datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') - last_time)

    if time_diff <= datetime.timedelta(seconds=0):
        # cut here
        break
    if first:
        lt_file = open('lasttime.txt', 'w')
        lt_file.write(time)
        lt_file.close()
        first = False

    if signal == u'ZAŁĄCZENIE':
        if message.get('zal') is None:
            message['zal'] = []
        message['zal'].append(settings.ZONES[zone_no])
    if signal == u'WYŁĄCZENIE':
        if message.get('wyl') is None:
            message['wyl'] = []
        message['wyl'].append(settings.ZONES[zone_no])
    if signal == u'KOMUNIKAT':
        if message.get('kom') is None:
            message['kom'] = []
        message['kom'].append(settings.ZONES[zone_no])
    if signal == u'WŁAMANIE':
        if message.get('wlam') is None:
            message['wlam'] = []
        message['wlam'].append(settings.ZONES[zone_no])
    if signal == u'NAPAD':
        message['napad'] = True  # specjalny przypadek, tutaj tylko fakt napadu, bez strefy

message_text = ''

if message.get('zal') is not None:
    if message_text != '':
        message_text += "\n"
    message_text += "ZALACZONO: " + ', '.join(message['zal'])
if message.get('wyl') is not None:
    if message_text != '':
        message_text += "\n" 
    message_text += "WYLACZONO: " + ', '.join(message['wyl'])
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

if message_text != '':
    if DEBUG:
        print message_text
    else:
        try:
            smsapi = SmsAPI()
            smsapi.set_username(settings.SMSAPI_LOGIN)
            smsapi.set_password(settings.SMSAPI_PASS)
            smsapi.service('sms').action('send')
            if settings.SMSAPI_PRO:
                smsapi.set_from(settings.SMSAPI_PRO_FROM)
            else:
                smsapi.set_eco(True)
            for phone in settings.PHONE_NUMBERS:
                smsapi.set_content(message_text.encode('utf-8'))
                smsapi.set_to(phone)
                smsapi.execute()
        except ApiError, e:
            print 'ERROR: %s - %s' % (e.code, e.message)
