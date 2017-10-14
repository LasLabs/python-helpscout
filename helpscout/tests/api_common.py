# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest


class ApiCommon(unittest.TestCase):

    def setUp(self):
        super(ApiCommon, self).setUp()
        self.mock_record = mock.MagicMock()
        self.mock_class = mock.MagicMock()
        self.mock_session = mock.MagicMock()
        self.mock_record.id = 1234

    def _test_method(self, cls, method_name, method_args=None, uri=None,
                     data=None, request_type=None, singleton=False,
                     out_type=None):
        """Helper to test an API method call."""

        if method_args is None:
            method_args = []

        with mock.patch.object(cls, '__new__') as new:

            method = getattr(cls, method_name)
            method(self.mock_session, *method_args)

            new.assert_called_once()

            call_args = new.call_args[0]
            call_kwargs = new.call_args[1]

            self.assertEqual(call_kwargs['session'], self.mock_session)

            if uri is not None:
                self.assertEqual(call_args[1], uri)

            if data is not None:
                try:
                    self.assertEqual(call_kwargs['data'], data.to_api())
                # Simple object, not a model
                except AttributeError:
                    self.assertEqual(call_kwargs['data'], data)

            if request_type is not None:
                self.assertEqual(call_kwargs['request_type'], request_type)

            if singleton:
                self.assertTrue(call_kwargs['singleton'])

            if out_type is not None:
                self.assertEqual(call_kwargs['out_type'], out_type)
