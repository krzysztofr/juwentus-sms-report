# -*- coding: utf-8 -*-

lines = {
    1: 'kont spizarnia',
    2: 'kont kuchnia L',
    3: 'kont kuchnia P',
    4: 'kont jadalnia',
    5: 'kont salon L',
    6: 'kont salon P',
    7: 'kont salon taras',
    8: 'kont gabinet',
    10: 'kont G schody',
    11: 'kont D schody',
    12: 'kont pralnia',
    13: 'kont lazienka duza',
    14: 'kont G korytarz',
    15: 'kont D korytarz',
    16: 'kont pok.1 L',
    17: 'kont pok.1 P',
    18: 'kont pok.2 L',
    19: 'kont pok.2 P',
    20: 'kont sypialnia L',
    21: 'kont sypialnia P',
    22: 'kont lazienka sypialnia',
    24: 'stlucz spizarnia',
    25: 'stlucz kuchnia',
    26: 'stlucz salon',
    27: 'Napad',
    28: 'stlucz pracownia',
    29: 'stlucz schody',
    30: 'stlucz pralnia',
    31: 'stlucz lazienka duza',
    32: 'stlucz korytarz',
    33: 'stlucz pok.1',
    34: 'stlucz pok.2',
    35: 'stlucz sypialnia',
    36: 'stlucz lazienka sypialnia',
    37: 'ruch przedsionek',
    38: 'ruch salon',
    39: 'ruch jadalnia',
    40: 'ruch gabinet',
    49: 'ruch garaz',
    50: 'ruch garaz',
    51: 'kont drzwi garaz',
    52: 'sabotaz',
    53: 'ruch korytarz gora P',
    54: 'ruch korytarz gora L'
}

zones = {
    1: 'pietro okna',
    3: 'pietro czujki',
    2: 'parter okna',
    4: 'parter czujki',
    5: 'garaz',
    6: 'salon czujki'
}

users = {
    3: 'Alice',
    6: 'John'
}

test_default = {
    'ZONES': zones,
    'LINES': lines,
    'USERS': users,
    'IGNORE_ACTIONS': (),
    'IGNORE_USERS': (),
    'IGNORE_ZAL_ZONES': (),
    'SMSAPI_LOGIN': 'nobody@example.com',
    'SMSAPI_PASS': 'secret_password',
    'SMSAPI_PRO_FROM': 'Alert',  # registered from name for "Pro" messages
    'SMSAPI_PRO': True,  # to use Pro or not?,
    'PHONE_NUMBERS': ('123456789', '987654321'),
    'EMAIL_SMTP_HOST': 'smtp.example.com',
    'EMAIL_SMTP_USER': 'example_user',
    'EMAIL_SMTP_PASS': 'secret_password',
    'EMAIL_SUBJECT': 'Test Subject.',
    'EMAIL_FROM': 'nobody@example.com',
    'EMAILS_TO': ('nobody@example.com', 'nobody2@example.com'),
}

test_ignore_user3 = {
    'ZONES': zones,
    'LINES': lines,
    'USERS': users,
    'IGNORE_ACTIONS': (),
    'IGNORE_USERS': (3,),
    'IGNORE_ZAL_ZONES': ()
}

test_ignore_zal = {
    'ZONES': zones,
    'LINES': lines,
    'USERS': users,
    'IGNORE_ACTIONS': ('zal',),
    'IGNORE_USERS': (),
    'IGNORE_ZAL_ZONES': ()
}

test_ignore_zal_garaz = {
    'ZONES': zones,
    'LINES': lines,
    'USERS': users,
    'IGNORE_ACTIONS': ('wyl',),
    'IGNORE_USERS': (),
    'IGNORE_ZAL_ZONES': (5,)
}