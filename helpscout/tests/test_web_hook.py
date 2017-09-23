# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import json
import unittest

from ..exceptions import HelpScoutSecurityException
from ..web_hook import HelpScoutWebHook
from ..web_hook.web_hook_event import WebHookEvent


class TestWebHook(unittest.TestCase):

    def setUp(self):
        super(TestWebHook, self).setUp()
        self.data_str = '{"firstName":"Jackie","lastName":"Chan",' \
                        '"email":"jackie.chan@somewhere.com",' \
                        '"gender":"male"}'
        self.data = json.loads(self.data_str)
        self.signature = '\n2iFmnzC8SCNVF/iNiMnSe19yceU=\n'
        self.bad_signature = '4+kjl2zB5OwZZjHznSTkD1/J208='
        self.hook = HelpScoutWebHook(secret_key='your secret key')

    def test_validate_signature_valid(self):
        """It should return True for valid signature."""
        self.assertTrue(
            self.hook.validate_signature(self.signature, self.data_str),
        )

    def test_validate_signature_invalid(self):
        """It should return False for invalid signature."""
        self.assertFalse(
            self.hook.validate_signature(self.bad_signature, self.data_str),
        )

    def test_receive_str_invalid(self):
        """It should raise on invalid signature from data string."""
        with self.assertRaises(HelpScoutSecurityException):
            self.hook.receive(None, self.signature, '{"nope": "1"}')

    def test_receive_returns_event(self):
        """Valid receive should return instantiated web hook event."""
        self.assertIsInstance(
            self.hook.receive(
                'customer.created', self.signature, self.data_str,
            ),
            WebHookEvent,
        )
