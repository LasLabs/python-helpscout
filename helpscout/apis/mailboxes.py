# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.mailbox import Mailbox


class Mailboxes(BaseApi):
    """This represents the ``Mailboxes`` Endpoint.

    The following aspects are implemented:
    * `List Mailboxes
      <http://developer.helpscout.net/help-desk-api/mailboxes/list/>`_
    * `Get Mailboxes
      <http://developer.helpscout.net/help-desk-api/mailboxes/get/>`_
    * `Get Folders
      <http://developer.helpscout.net/help-desk-api/mailboxes/folders/>`_
    """

    __object__ = Mailbox

    @classmethod
    def get(cls, session, mailbox_id):
        """Return a specific mailbox.

        Args:
            session (requests.Session): Authenticated requests Session.
            mailbox_id (int): The ID of the mailbox to get.

        Returns:
            Mailbox: A mailbox singleton, if existing.
            None: If no match for the ID.
        """
        return cls(
            '/mailboxes/%d.json' % mailbox_id,
            singleton=True,
            session=session,
        )

    @classmethod
    def list(cls, session):
        """List the mailboxes.

        Args:
            session (requests.Session): Authenticated requests Session.

        Returns:
            RequestPaginator of Mailbox: Mailboxes iterator.
        """
        return cls('/mailboxes.json', session=session)

    @classmethod
    def list_folders(cls, session, mailbox_or_id):
        """List the folders for the mailbox.

        Args:
            mailbox_or_id (Mailbox or int): Mailbox of the ID of the mailbox
            to get the folders for.

        Returns:
            RequestPaginator of Folder: Folders iterator.
        """
        if isinstance(mailbox_or_id, Mailbox):
            mailbox_or_id = mailbox_or_id.id
        return cls(
            '/mailboxes/%d/folders.json' % mailbox_or_id,
            session=session,
        )
