# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.person import Person
from ..models.user import User


class Teams(BaseApi):
    """This represents the ``Teams`` Endpoint.

    The following aspects are implemented:

    * `List Teams
      <http://developer.helpscout.net/help-desk-api/teams/list/>`_
      (:func:`helpscout.apis.teams.Teams.list`)
    * `Get Teams
      <http://developer.helpscout.net/help-desk-api/teams/get/>`_
      (:func:`helpscout.apis.teams.Teams.get`)
    * `Get Team Members
      <http://developer.helpscout.net/help-desk-api/teams/team-members/>`_
      (:func:`helpscout.apis.teams.Teams.get_members`)
    """

    __object__ = Person

    @classmethod
    def get(cls, session, team_id):
        """Return a specific team.

        Args:
            session (requests.sessions.Session): Authenticated session.
            team_id (int): The ID of the team to get.

        Returns:
            helpscout.models.Person: A person singleton representing the team,
                if existing. Otherwise ``None``.
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
            session (requests.sessions.Session): Authenticated session.

        Returns:
            RequestPaginator(output_type=helpscout.models.Person): Person
                iterator representing the teams.
        """
        return cls('/teams.json', session=session)

    @classmethod
    def get_members(cls, session, team_or_id):
        """List the members for the team.

        Args:
            team_or_id (helpscout.models.Person or int): Team or the ID of
                the team to get the folders for.

        Returns:
            RequestPaginator(output_type=helpscout.models.Users): Users
                iterator.
        """
        if isinstance(team_or_id, Person):
            team_or_id = team_or_id.id
        return cls(
            '/teams/%d/members.json' % team_or_id,
            session=session,
            out_type=User,
        )
