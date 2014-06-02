# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText


def send(message, settings):

    s = smtplib.SMTP(settings['EMAIL_SMTP_HOST'])
    s.login(settings['EMAIL_SMTP_USER'], settings['EMAIL_SMTP_PASS'])

    for to in settings['EMAILS_TO']:
        msg = MIMEText(message)
        msg['Subject'] = settings['EMAIL_SUBJECT']
        msg['From'] = settings['EMAIL_FROM']
        msg['To'] = to
        s.sendmail(settings['EMAIL_FROM'], [to], msg.as_string())

    s.quit()
