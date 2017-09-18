# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.user import User


class Users(BaseApi):
    """This represents the ``Users`` Endpoint.

    The following aspects are implemented:
    * `List Users
      <http://developer.helpscout.net/help-desk-api/users/list/>`_
    * `Get Users
      <http://developer.helpscout.net/help-desk-api/users/get/>`_
    * `Get Folders
      <http://developer.helpscout.net/help-desk-api/users/folders/>`_
    """

    __object__ = User

    @classmethod
    def get(cls, session, user_id):
        """Return a specific user.

        Args:
            session (requests.Session): Authenticated requests Session.
            user_id (int): The ID of the user to get.

        Returns:
            User: A user singleton, if existing.
            None: If no match for the ID.
        """
        return cls(
            '/users/%d.json' % user_id,
            singleton=True,
            session=session,
        )

    @classmethod
    def get_me(cls, session):
        """Return the current user.

        Args:
            session (requests.Session): Authenticated requests Session.

        Returns:
            User: A user singleton
        """
        return cls(
            '/users/me.json',
            singleton=True,
            session=session,
        )

    @classmethod
    def list(cls, session):
        """List the users.

        Args:
            session (requests.Session): Authenticated requests Session.

        Returns:
            RequestPaginator of User: Users iterator.
        """
        return cls('/users.json', session=session)

    @classmethod
    def find_in_mailbox(cls, session, mailbox_or_id):
        """Get the users that are associated to a Mailbox.

        Args:
            session (requests.Session): Authenticated requests Session.
            mailbox_or_id (MailboxRef or int): Mailbox of the ID of the
            mailbox to get the folders for.

        Returns:
            RequestPaginator of User: Users iterator.
        """
        if isinstance(mailbox_or_id, User):
            mailbox_or_id = mailbox_or_id.id
        return cls(
            '/mailboxes/%d/users.json' % mailbox_or_id,
            session=session,
        )
