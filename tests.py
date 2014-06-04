# -*- coding: utf-8 -*-

from juwparser import parse, get_last_time, timestampize
from senders import e_mail, file as s_file, sms_api

from test_settings import test_ignore_user3 as settings_ignore_user3
from test_settings import test_ignore_zal as settings_ignore_zal
from test_settings import test_default as settings_default
from test_settings import test_ignore_zal_garaz as settings_ignore_zal_garaz

import unittest
import os
import datetime
from email.mime.text import MIMEText

import mock


class JuwparserTestCase(unittest.TestCase):

    lt_filename = "lasttime_test.txt"
    last_time = "2014-04-24 00:00:00"

    def setUp(self):
        with open(self.lt_filename, 'w') as f:
            f.write(self.last_time)

        with open('testdata/log.html', 'r') as td_f:
            self.testdata1 = td_f.read()

        with open('testdata/log2.html', 'r') as td_f:
            self.testdata2 = td_f.read()

    def tearDown(self):
        os.remove(self.lt_filename)

    def test_get_last_time(self):
        last_time = get_last_time(self.lt_filename)

        self.assertEqual(last_time, datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), 'Last time value is different than expected ' + self.last_time +'.')

    def test_parse_ignore_user3(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_user3)

        self.assertEqual(parsed, "ZALACZONO (John): garaz, parter czujki, parter okna, pietro okna, parter czujki, garaz, parter okna, pietro okna", "User's 3 actions not ignored or wrong contents of the input file.")

    def test_parse_ignore_zal(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_zal)

        self.assertEqual(parsed, "WYLACZONO (Alice): garaz, parter czujki, parter okna, pietro okna, parter czujki, garaz, pietro czujki, parter okna, pietro okna, parter czujki, garaz, pietro czujki, parter okna, pietro okna, garaz, parter czujki, parter okna, pietro okna", "'zal' action not ignored or wrong contents of the input file.")

    def test_wlamanie(self):

        parsed = parse(html=self.testdata2, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("WLAMANIE: parter czujki", parsed, "No WLAMANIE action reported or wrong contents of the input file.")

    def test_napad(self):

        parsed = parse(html=self.testdata2, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("NAPAD!", parsed, "No NAPAD action reported or wrong contents of the input file.")

    def test_user_names(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("ZALACZONO (Alice, John)", parsed, "No user 3 and 6 ZALACZONO action present or wrong contents of the input file.")
        self.assertIn("WYLACZONO (Alice)", parsed, "No user 3 ZALACZONO action present or wrong contents of the input file.")

    def test_garaz_in_zal(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_default)

        self.assertIn("garaz", parsed, "Zone 'garaz' should be in the results.")

    def test_ignore_garaz_in_zal(self):

        parsed = parse(html=self.testdata1, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_zal_garaz)

        self.assertNotIn("garaz", parsed, "Zone 'garaz' in the results, where it shouldn't be.")

    @mock.patch('juwparser.strftime')
    def test_timestampize(self, mock_strftime):

        text = "line1\nline2\nline3"

        mock_strftime.return_value = '2014-05-13 21:00:00'

        text_timestamped = timestampize(text)

        self.assertEqual(text_timestamped, '[2014-05-13 21:00:00] line1\n[2014-05-13 21:00:00] line2\n[2014-05-13 21:00:00] line3', 'Timestampize returns result in wrong format. No timestamps?')

    @mock.patch('senders.sms_api.SmsAPI')
    def test_sender_sms_api(self, mock_smsapi):
        smsapi_instance = mock_smsapi.return_value

        test_message = 'This is a test message.'

        sms_api.send(message=test_message, settings=settings_default)

        smsapi_instance.set_username.assert_called_with(settings_default['SMSAPI_LOGIN'])
        smsapi_instance.set_password.assert_called_with(settings_default['SMSAPI_PASS'])
        if settings_default['SMSAPI_PRO']:
            smsapi_instance.set_from.assert_called_with(settings_default['SMSAPI_PRO_FROM'])
        else:
            smsapi_instance.set_eco.assert_called_with(True)
        smsapi_instance.set_content.assert_called_with(test_message)
        for number in settings_default['PHONE_NUMBERS']:
            smsapi_instance.set_to.assert_any_call(number)
        self.assertEqual(smsapi_instance.execute.call_count, len(settings_default['PHONE_NUMBERS']))

    @mock.patch('senders.e_mail.smtplib.SMTP')
    def test_sender_email(self, mock_smtp):

        test_message = 'This is a test message.'

        e_mail.send(message=test_message, settings=settings_default)

        mock_smtp.assert_called_with(settings_default['EMAIL_SMTP_HOST'])

        smtp_instance = mock_smtp.return_value

        smtp_instance.login.assert_called_with(settings_default['EMAIL_SMTP_USER'], settings_default['EMAIL_SMTP_PASS'])

        for to in settings_default['EMAILS_TO']:
            msg = MIMEText(test_message)
            msg['Subject'] = settings_default['EMAIL_SUBJECT']
            msg['From'] = settings_default['EMAIL_FROM']
            msg['To'] = to

            smtp_instance.sendmail.assert_any_call(settings_default['EMAIL_FROM'], [to], msg.as_string())

        self.assertEqual(smtp_instance.sendmail.call_count, len(settings_default['EMAILS_TO']))
        self.assertEqual(smtp_instance.quit.call_count, 1)

    @mock.patch('juwparser.strftime')
    def test_sender_file(self, mock_strftime):
        mo = mock.mock_open()
        test_message = 'This is a test message.'

        mock_strftime.return_value = '2014-05-13 21:00:00'

        with mock.patch('senders.file.open', mo, create=True):
            s_file.send(message=test_message, settings=settings_default)
            mo.assert_called_once_with(settings_default['FILE_SAVE'], 'a')
            mo().write.assert_any_call(timestampize(test_message))
            mo().write.assert_any_call("\n")

