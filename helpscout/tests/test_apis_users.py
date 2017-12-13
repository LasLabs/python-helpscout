# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon, recorder


class TestApisUsers(ApiCommon):
    """Tests the Users API endpoint."""

    def setUp(self):
        super(TestApisUsers, self).setUp()
        self.__endpoint__ = self.api.Users

    @recorder.use_cassette()
    def test_apis_users_get(self):
        """It should return the user."""
        self._test_get(self._get_user())

    @recorder.use_cassette()
    def test_apis_users_delete(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.delete(self._get_user())

    @recorder.use_cassette()
    def test_apis_users_update(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.update(self._get_user())

    @recorder.use_cassette()
    def test_apis_users_create(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.create(self._get_user())

    @recorder.use_cassette()
    def test_apis_users_list(self):
        """It should list the users in the user."""
        self._test_list()

    @recorder.use_cassette()
    def test_apis_users_search(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.search([], None)

    @recorder.use_cassette()
    def test_apis_users_get_me(self):
        """It should return the current users."""
        self.assertEqual(self.api.Users.get_me().id, self._get_user().id)

    @recorder.use_cassette()
    def test_apis_users_find_in_mailbox(self):
        """It should return the users associated with the mailbox."""
        results = list(
            self.api.Users.find_in_mailbox(self._get_mailbox_ref())
        )
        self._assert_results(results)
        self.assertIn(self._get_user().id, [u.id for u in results])
