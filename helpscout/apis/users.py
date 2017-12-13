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
      (:func:`helpscout.apis.users.Users.list`)
    * `Get Users
      <http://developer.helpscout.net/help-desk-api/users/get/>`_
      (:func:`helpscout.apis.users.Users.get`)
    * `Get Current User
      <http://developer.helpscout.net/help-desk-api/users/get/>`_
      (:func:`helpscout.apis.users.Users.get_me`)
    * `List Users By Mailbox
      <http://developer.helpscout.net/help-desk-api/users/mailbox-users/>`_
      (:func:`helpscout.apis.users.Users.find_in_mailbox`)
    """

    __object__ = User
    __endpoint__ = 'users'
    __implements__ = ['get', 'list']

    @classmethod
    def get_me(cls, session):
        """Return the current user.

        Args:
            session (requests.sessions.Session): Authenticated session.

        Returns:
            helpscout.models.User: A user singleton
        """
        return cls(
            '/users/me.json',
            singleton=True,
            session=session,
        )

    @classmethod
    def find_in_mailbox(cls, session, mailbox_or_id):
        """Get the users that are associated to a Mailbox.

        Args:
            session (requests.sessions.Session): Authenticated session.
            mailbox_or_id (MailboxRef or int): Mailbox of the ID of the
                mailbox to get the folders for.

        Returns:
            RequestPaginator(output_type=helpscout.models.User): Users
                iterator.
        """
        if hasattr(mailbox_or_id, 'id'):
            mailbox_or_id = mailbox_or_id.id
        return cls(
            '/mailboxes/%d/users.json' % mailbox_or_id,
            session=session,
        )
