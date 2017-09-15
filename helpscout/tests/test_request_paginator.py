# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from contextlib import contextmanager

try:
    import mock
except ImportError:
    mock = unittest.mock

from ..request_paginator import RequestPaginator


class TestRequestPaginator(unittest.TestCase):

    def setUp(self):
        self.vals = {
            'endpoint': 'endpoint',
            'data': {'param': 1},
            'output_type': dict,
        }
        self.test_responses = [
            {
                'page': 1,
                'pages': 3,
                'items': [{
                    'page': 1,
                }],
            },
            {
                'page': 2,
                'pages': 3,
                'items': [{
                    'page': 2,
                }],
            },
            {
                'page': 3,
                'pages': 3,
                # This one emulates a singleton
                'item': {
                    'page': 3,
                },
            },
        ]
        self.paginator = RequestPaginator(**self.vals)

    @contextmanager
    def mock_session(self, response_code=200, responses=None):
        if responses is None:
            responses = self.test_responses
        with mock.patch.object(self.paginator, 'session') as session:
            response = mock.MagicMock()
            response.status_code = response_code
            response.json.side_effect = responses
            session.get.return_value = response
            session.post.return_value = response
            yield session

    def test_init_attrs(self):
        """ It should correctly assign instance attributes. """
        attrs = {
            attr: getattr(self.paginator, attr) for attr in self.vals.keys()
        }
        self.assertDictEqual(attrs, self.vals)

    @mock.patch('helpscout.request_paginator.requests')
    def test_init_session(self, requests):
        """ It should initialize a requests session. """
        paginator = RequestPaginator(**self.vals)
        self.assertEqual(paginator.session, requests.Session())

    def test_get_gets(self):
        """ It should call the session with proper args. """
        params = {'param_test': 23234}
        with self.mock_session() as session:
            self.paginator.get(params)
            session.get.assert_called_once_with(
                url=self.vals['endpoint'],
                params=params,
                verify=True,
            )

    def test_get_return(self):
        """ It should return the json decoded response. """
        with self.mock_session() as _:
            res = self.paginator.get({})
            self.assertEqual(len(res), 1)
            self.assertDictEqual(res[0], self.test_responses[0]['items'][0])

    def test_post_posts(self):
        """ It should call the session with proper args. """
        params = {'param_test': 23234}
        with self.mock_session() as session:
            self.paginator.post(params)
            session.post.assert_called_once_with(
                url=self.vals['endpoint'],
                json=params,
                verify=True,
            )

    def test_post_return(self):
        """ It should return the json decoded response. """
        with self.mock_session() as _:
            res = self.paginator.post({})
            self.assertEqual(len(res), 1)
            self.assertDictEqual(res[0], self.test_responses[0]['items'][0])

    def test_call_get(self):
        """It should get when the request type is GET."""
        params = {'param_test': 23234}
        self.paginator.request_type = self.paginator.GET
        with mock.patch.object(self.paginator, 'get') as get:
            self.paginator.call(params)
        get.assert_called_once_with(params)

    def test_call_post(self):
        """It should post when the request type is POST."""
        params = {'param_test': 23234}
        self.paginator.request_type = self.paginator.POST
        with mock.patch.object(self.paginator, 'post') as post:
            self.paginator.call(params)
        post.assert_called_once_with(params)

    def test_iter(self):
        """ It should iterate until the end & yield data. """
        with self.mock_session() as session:
            session.get().json.side_effect = self.test_responses
            res = list(self.paginator)
            expect = [{'page': 1}, {'page': 2}, {'page': 3}]
            self.assertEqual(res, expect)
