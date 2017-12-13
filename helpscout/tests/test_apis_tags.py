# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon, recorder


class TestApisTags(ApiCommon):
    """Tests the Tags API endpoint."""

    def setUp(self):
        super(TestApisTags, self).setUp()
        self.__endpoint__ = self.api.Tags

    @recorder.use_cassette()
    def test_apis_tags_get(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.update(None)

    @recorder.use_cassette()
    def test_apis_tags_delete(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.delete(None)

    @recorder.use_cassette()
    def test_apis_tags_update(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.update(None)

    @recorder.use_cassette()
    def test_apis_tags_create(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.create(None)

    @recorder.use_cassette()
    def test_apis_tags_list(self):
        """It should list the tags in the tag."""
        self._test_list()

    @recorder.use_cassette()
    def test_apis_tags_search(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.search([], None)
