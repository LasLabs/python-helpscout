# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon, recorder


class TestApisTeams(ApiCommon):
    """Tests the Teams API endpoint."""

    def setUp(self):
        super(TestApisTeams, self).setUp()
        self.__endpoint__ = self.api.Teams

    @recorder.use_cassette()
    def test_apis_teams_get(self):
        """It should return the team."""
        self._test_get(self._get_team())

    @recorder.use_cassette()
    def test_apis_teams_delete(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.delete(None)

    @recorder.use_cassette()
    def test_apis_teams_update(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.update(None)

    @recorder.use_cassette()
    def test_apis_teams_create(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.create(None)

    @recorder.use_cassette()
    def test_apis_teams_list(self):
        """It should list the teams in the team."""
        self._test_list()

    @recorder.use_cassette()
    def test_apis_teams_search(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.search([], None)

    @recorder.use_cassette()
    def test_apis_teams_get_members(self):
        """It should get the team members."""
        team = self._get_team()
        user_ids = [u.id for u in self.api.Teams.get_members(team)]
        self.assertIn(self._get_user().id, user_ids)
