# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon, recorder


class TestApisMailboxes(ApiCommon):
    """Tests the Mailboxes API endpoint."""

    def setUp(self):
        super(TestApisMailboxes, self).setUp()
        self.__endpoint__ = self.api.Mailboxes

    @recorder.use_cassette()
    def test_apis_mailboxes_get(self):
        """It should return the mailbox."""
        self._test_get(self._get_mailbox_ref())

    @recorder.use_cassette()
    def test_apis_mailboxes_delete(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.delete(self._get_mailbox_ref())

    @recorder.use_cassette()
    def test_apis_mailboxes_update(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.update(self._get_mailbox_ref())

    @recorder.use_cassette()
    def test_apis_mailboxes_create(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.create(self._get_mailbox_ref())

    @recorder.use_cassette()
    def test_apis_mailboxes_list(self):
        """It should list the mailboxes in the mailbox."""
        self._test_list()

    @recorder.use_cassette()
    def test_apis_mailboxes_search(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.search([], None)
