# -*- coding: utf-8 -*-

from juwparser import parse, get_last_time

from test_settings import test_ignore_user3 as settings_ignore_user3, test_ignore_zal as settings_ignore_zal

import unittest
import os
import datetime


class JuwparserTestCase(unittest.TestCase):

    lt_filename = "lasttime_test.txt"
    last_time = "2014-04-24 00:00:00"

    def setUp(self):
        with open(self.lt_filename, 'w') as f:
            f.write(self.last_time)

        with open('testdata/log.html', 'r') as td_f:
            self.testdata = td_f.read()

    def tearDown(self):
        os.remove(self.lt_filename)

    def test_get_last_time(self):
        last_time = get_last_time(self.lt_filename)

        self.assertEqual(last_time, datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), 'Last time value is different than expected.')

    def test_parse_ignore_user3(self):

        parsed = parse(html=self.testdata, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_user3)

        self.assertEqual(parsed, "ZALACZONO: garaz, parter czujki, parter okna, pietro okna, parter czujki, garaz, parter okna, pietro okna", "Result other than expected.")

    def test_parse_ignore_zal(self):

        parsed = parse(html=self.testdata, last_time=datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), last_time_filename=self.lt_filename, settings=settings_ignore_zal)

        self.assertEqual(parsed, "WYLACZONO: garaz, parter czujki, parter okna, pietro okna, parter czujki, garaz, pietro czujki, parter okna, pietro okna, parter czujki, garaz, pietro czujki, parter okna, pietro okna, garaz, parter czujki, parter okna, pietro okna", "Result other than expected.")
