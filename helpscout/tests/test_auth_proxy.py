# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

try:
    import mock
except ImportError:
    mock = unittest.mock

from .. import AuthProxy


class EndTestException(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(EndTestException, self).__init__()


class ApiClass(object):

    @classmethod
    def proxied(cls, session=None):
        raise EndTestException(session=session)

    @classmethod
    def not_proxied(cls, *args, **kwargs):
        raise Exception()


class TestAuthProxy(unittest.TestCase):

    SESSION = 'session'

    def new_proxy(self, session=SESSION, proxy_class=ApiClass):
        return AuthProxy(session, proxy_class)

    def test_init_bad_api_class(self):
        """It should assert API class is a class."""
        with self.assertRaises(AssertionError):
            AuthProxy(None, 'not a class')

    def test_init_sets_session(self):
        """It should set the session instance var."""
        proxy = self.new_proxy()
        self.assertEqual(proxy.session, self.SESSION)

    def test_init_sets_proxy_class(self):
        """It should set the proxy_class instance var."""
        proxy = self.new_proxy()
        self.assertEqual(proxy.proxy_class, ApiClass)

    def test_getattr_injects_session(self):
        """It should inject the session into the proxied method."""
        proxy_method = self.new_proxy().proxied
        try:
            proxy_method()
        except EndTestException as e:
            self.assertEqual(e.kwargs['session'], self.SESSION)

    def test_getattr_whitelist(self):
        """It should not proxy methods that are in the whitelist."""
        proxy = self.new_proxy()
        proxy.METHOD_NO_PROXY.append('not_proxied')
        with self.assertRaises(AttributeError):
            proxy.not_proxied()
