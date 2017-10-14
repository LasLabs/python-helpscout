# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon

from ..apis.web_hook import WebHook


class TestApiWebHook(ApiCommon):

    def test_create(self):
        self._test_method(
            WebHook, 'create', [self.mock_record], '/hooks.json',
            None, 'post', False,
        )
