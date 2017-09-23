# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from datetime import datetime

from ..domain import Domain


class TestDomain(unittest.TestCase):

    def test_init_adds_queries(self):
        """It should add queries if defined."""
        with mock.patch.object(Domain, 'add_query') as add:
            Domain(['expect'], 'test')
            add.assert_called_once_with('expect', 'test')

    def test_from_tuple(self):
        """It should return the proper domain."""
        data = [('status', 'active'),
                ('number', 1234),
                ('modified_at', datetime(2017, 1, 1), datetime(2017, 1, 2)),
                ('subject', 'Test1'),
                'OR',
                ('subject', 'Test2')]
        res = Domain.from_tuple(data)
        self.assertEqual(
            str(res),
            '('
            'status:"active" '
            'AND number:1234 '
            'AND modifiedAt:[2017-01-01T00:00:00Z TO 2017-01-02T00:00:00Z] '
            'AND subject:"Test1" '
            'OR subject:"Test2"'
            ')',
        )
