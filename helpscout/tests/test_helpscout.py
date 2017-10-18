# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from .. import AuthProxy
from .. import HelpScout
from ..apis import __all__ as all_apis


class TestHelpScout(unittest.TestCase):

    API_KEY = 'test key'

    def setUp(self):
        super(TestHelpScout, self).setUp()
        self.hs = HelpScout(self.API_KEY)

    def test_init_session(self):
        """It should build a session with the proper authentication."""
        self.assertEqual(self.hs.session.auth.username, self.API_KEY)

    def test_load_apis(self):
        """It should load all available APIs."""
        self.assertEqual(len(self.hs.__apis__), len(all_apis))

    def test_api_instance_attributes(self):
        """It should properly set all of the API instance attributes."""
        for api_name, api in self.hs.__apis__.items():
            self.assertEqual(getattr(self.hs, api_name), api)

    def test_api_auth_proxy(self):
        """It should wrap the APIs in an AuthProxy."""
        for api in self.hs.__apis__.values():
            self.assertIsInstance(api, AuthProxy)
