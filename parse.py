# -*- coding: utf-8 -*-

from smsapi.client import SmsAPI
from smsapi.responses import ApiError

from settings import default as settings

from juwparser import parse, get_log, get_last_time

try:
    DEBUG = settings['DEBUG']
except NameError:
    DEBUG = False


message_text = parse(html=get_log(settings=settings), last_time=get_last_time(), settings=settings)

if message_text != '':
    if DEBUG:
        print message_text
    else:
        try:
            smsapi = SmsAPI()
            smsapi.set_username(settings['SMSAPI_LOGIN'])
            smsapi.set_password(settings['SMSAPI_PASS'])
            smsapi.service('sms').action('send')
            if settings.SMSAPI_PRO:
                smsapi.set_from(settings['SMSAPI_PRO_FROM'])
            else:
                smsapi.set_eco(True)
            for phone in settings['PHONE_NUMBERS']:
                smsapi.set_content(message_text.encode('utf-8'))
                smsapi.set_to(phone)
                smsapi.execute()
        except ApiError, e:
            print 'ERROR: %s - %s' % (e.code, e.message)
