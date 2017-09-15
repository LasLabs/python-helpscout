# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.user import User


class Teams(BaseApi):
    """This represents the ``Teams`` Endpoint.

    The following aspects are implemented:
    * `List Teams
      <http://developer.helpscout.net/help-desk-api/teams/list/>`_
    * `Get Teams
      <http://developer.helpscout.net/help-desk-api/teams/get/>`_
    * `Get Team Members
      <http://developer.helpscout.net/help-desk-api/teams/team-members/>`_
    """

    __object__ = User

    @classmethod
    def get(cls, session, team_id):
        """Return a specific team.

        Args:
            session (requests.Session): Authenticated requests Session.
            team_id (int): The ID of the team to get.

        Returns:
            Team: A team singleton, if existing.
            None: If no match for the ID.
        """
        return cls(
            '/teams/%d.json' % team_id,
            singleton=True,
            session=session,
        )

    @classmethod
    def list(cls, session):
        """List the teams.

        Args:
            session (requests.Session): Authenticated requests Session.

        Returns:
            RequestPaginator of Team: Teams iterator.
        """
        return cls('/teams.json', session=session)

    @classmethod
    def list_members(cls, session, team_or_id):
        """List the members for the team.

        Args:
            team_or_id (Team or int): Team of the ID of the team
            to get the folders for.

        Returns:
            RequestPaginator of User: Users iterator.
        """
        if isinstance(team_or_id, Team):
            team_or_id = team_or_id.id
        return cls(
            '/teams/%d/members.json' % team_or_id,
            session=session,
        )
