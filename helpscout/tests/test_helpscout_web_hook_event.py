# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..models import Customer
from ..web_hook import HelpScoutWebHookEvent


class TestHelpScoutWebHookEvent(unittest.TestCase):

    def setUp(self):
        super(TestHelpScoutWebHookEvent, self).setUp()
        self.event_type = 'customer.created'
        self.data = {
            'gender': 'male',
            'first_name': 'Test',
            'last_name': 'Dude',
            'type': 'customer',
        }
        self.api_data = {
            'gender': self.data['gender'],
            'firstName': self.data['first_name'],
            'lastName': self.data['last_name'],
            'type': self.data['type'],
        }

    def _validate_record(self, record):
        self.assertIsInstance(record.record, Customer)
        for key, val in self.data.items():
            self.assertEqual(getattr(record.record, key), val)

    def test_record_from_data(self):
        """It should create a correct record from the API data."""
        self._validate_record(
            HelpScoutWebHookEvent(
                event_type=self.event_type, record=self.api_data,
            ),
        )

    def test_record_from_record(self):
        """It should pass through a pre-existing record."""
        record = Customer(**self.data)
        self._validate_record(
            HelpScoutWebHookEvent(
                event_type=self.event_type, record=record,
            ),
        )
