# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
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

    @mock.patch('helpscout.WebHook')
    def test_web_hook_init(self, WebHook):
        """It should initialize a web hook using the API key."""
        self.hs.web_hook()
        WebHook.assert_called_once_with(self.API_KEY)

    @mock.patch('helpscout.WebHook')
    def test_web_hook_cache(self, WebHook):
        """It should use the cached web hook the second time around."""
        self.hs.web_hook()
        self.hs.web_hook()
        WebHook.assert_called_once_with(self.API_KEY)

    @mock.patch('helpscout.WebHook')
    def test_web_hook_pass_through(self, WebHook):
        """It should pass args and kwargs through to receive method."""
        args = [1, 2, 3]
        kwargs = {'test1': 'derp', 'test2': True}
        self.hs.web_hook(*args, **kwargs)
        WebHook().receive.assert_called_once_with(*args, **kwargs)

    @mock.patch('helpscout.WebHook')
    def test_web_hook_return(self, WebHook):
        """It should return the receive method on a new web hook."""
        res = self.hs.web_hook()
        self.assertEqual(res, WebHook().receive())
