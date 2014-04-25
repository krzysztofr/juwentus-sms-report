# -*- coding: utf-8 -*-

from juwparser import parse, get_log, get_last_time

import unittest
import os
import datetime

class JuwparserTestCase(unittest.TestCase):

    lt_filename = "lasttime_test.txt"
    last_time = "2014-04-25 09:00:00"

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

    def test_parse(self):

        parsed = parse(self.testdata, datetime.datetime.strptime(self.last_time, '%Y-%m-%d %H:%M:%S'), self.lt_filename)

        self.assertEqual(parsed, "ZALACZONO: garaz, parter czujki, pietro okna, pietro czujki, parter okna", "Result other than expected.")