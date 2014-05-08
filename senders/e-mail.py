# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText


def send(message, settings):

    s = smtplib.SMTP(settings['EMAIL_SMTP_HOST'])
    s.login(settings['EMAIL_SMTP_USER'], settings['EMAIL_SMTP_PASS'])

    msg = MIMEText(message)
    msg['Subject'] = settings['EMAIL_SUBJECT']
    msg['From'] = settings['EMAIL_FROM']
    msg['To'] = settings['EMAIL_TO']
    s.sendmail(settings['EMAIL_FROM'], [settings['EMAIL_TO']], msg.as_string())

    s.quit()
