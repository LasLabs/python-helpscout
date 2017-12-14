# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.folder import Folder
from ..models.mailbox import Mailbox


class Mailboxes(BaseApi):
    """This represents the ``Mailboxes`` Endpoint.

    The following aspects are implemented:

    * `List Mailboxes
      <http://developer.helpscout.net/help-desk-api/mailboxes/list/>`_
      (:func:`helpscout.apis.mailboxes.Mailboxes.list`)
    * `Get Mailboxes
      <http://developer.helpscout.net/help-desk-api/mailboxes/get/>`_
      (:func:`helpscout.apis.mailboxes.Mailboxes.get`)
    * `Get Folders
      <http://developer.helpscout.net/help-desk-api/mailboxes/folders/>`_
      (:func:`helpscout.apis.mailboxes.Mailboxes.get_folders`)
    """

    __object__ = Mailbox
    __endpoint__ = 'mailboxes'
    __implements__ = ['get', 'list']

    @classmethod
    def list(cls, session):
        """List the mailboxes.

        Args:
            session (requests.sessions.Session): Authenticated session.

        Returns:
            RequestPaginator(output_type=helpscout.models.Mailbox): Mailboxes
                iterator.
        """
        return cls('/mailboxes.json', session=session)

    @classmethod
    def get_folders(cls, session, mailbox_or_id):
        """List the folders for the mailbox.

        Args:
            mailbox_or_id (helpscout.models.Mailbox or int): Mailbox or the ID
                of the mailbox to get the folders for.

        Returns:
            RequestPaginator(output_type=helpscout.models.Folder): Folders
                iterator.
        """
        if isinstance(mailbox_or_id, Mailbox):
            mailbox_or_id = mailbox_or_id.id
        return cls(
            '/mailboxes/%d/folders.json' % mailbox_or_id,
            session=session,
            out_type=Folder,
        )
