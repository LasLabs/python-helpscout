# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.conversation import Conversation
from ..models.search_conversation import SearchConversation
from ..models.thread import Thread

from ..request_paginator import RequestPaginator


class Conversations(BaseApi):
    """This represents the ``Conversations`` Endpoint.

    The following aspects are implemented:

    * `List Conversations
      <http://developer.helpscout.net/help-desk-api/conversations/list/>`_
      (:func:`~conversations.Conversation.list`)
    * `Search Conversations
      <http://developer.helpscout.net/help-desk-api/search/conversations/>`_
      (:func:`~conversations.Conversation.search`)
    * `Get Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/get/>`_
      (:func:`~conversations.Conversation.get`)
    * `Create Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/create/>`_
      (:func:`~conversations.Conversation.create`)
    * `Update Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/update/>`_
      (:func:`~conversations.Conversation.update`)
    * `Delete Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/delete/>`_
      (:func:`~conversations.Conversation.delete`)
    * `Create Thread
      <http://developer.helpscout.net/help-desk-api/conversations/
      create-thread/>`_
      (:func:`~conversations.Conversation.create_thread`)
    * `Update Thread
      <http://developer.helpscout.net/help-desk-api/conversations/
      update-thread/>`_
      (:func:`~conversations.Conversation.update_thread`)
    """

    __object__ = Conversation

    @classmethod
    def create(cls, session, conversation, imported=False, auto_reply=False,
               _reload=False):
        """Create a conversation.

        Please note that conversation cannot be created with more than 100
        threads, if attempted the API will respond with HTTP 412.

        Args:
            session (requests.Session): Authenticated requests Session.
            conversation (Conversation): The conversation to be created.
            imported (bool): The ``imported`` request parameter enables
             conversations to be created for historical purposes (i.e.
             if moving from a different platform, you can import your
             history). When ``imported`` is set to ``True``, no outgoing
             emails or notifications will be generated.
            auto_reply (bool): The ``auto_reply`` request parameter enables
             auto replies to be sent when a conversation is created via the
             API. When ``auto_reply`` is set to ``True``, an auto reply will
             be sent as long as there is at least one ``customer`` thread in the
             conversation.
            _reload (bool, optional): Set this request parameter to ``True``
             to return the created conversation in the response.

        Returns:
            bool: Success status, if ``_reload`` is ``False``.
            Conversation: Newly created conversation, if ``_reload`` is
             ``True``.
        """
        data = {
            'conversation': conversation.to_api(),
            'imported': imported,
            'auto_reply': auto_reply,
            'reload': _reload,
        }
        return cls(
            '/conversations.json',
            data=data,
            request_type=RequestPaginator.POST,
            singleton=True,
            session=session,
        )

    @classmethod
    def create_thread(cls, session, conversation, thread, imported=False,
                      _reload=False):
        """Create a conversation thread.

        Please note that threads cannot be added to conversations with 100 threads
        (or more), if attempted the API will respond with HTTP 412.

        Args:
            conversation (Conversation): The conversation that the thread is
             being added to.
            session (requests.Session): Authenticated requests Session.
            thread (Thread): The thread to be created.
            imported (bool): The ``imported`` request parameter enables
             conversations to be created for historical purposes (i.e.
             if moving from a different platform, you can import your
             history). When ``imported`` is set to ``True``, no outgoing
             emails or notifications will be generated.
            _reload (bool, optional): Set this request parameter to ``True``
             to return the created conversation in the response.

        Returns:
            bool: Success status, if ``_reload`` is ``False``.
            Thread: Newly created thread, if ``_reload`` is ``True``.
        """
        data = {
            'thread': thread.to_api(),
            'imported': imported,
            'reload': _reload,
        }
        return cls(
            '/conversations/%s.json' % conversation.id,
            data=data,
            request_type=RequestPaginator.POST,
            singleton=True,
            session=session,
            object=Thread,
        )

    @classmethod
    def delete(cls, session, conversation):
        """Delete a conversation.

        Args:
            session (requests.Session): Authenticated requests Session.
            conversation (Conversation): The conversation to be deleted.

        Returns:
            bool: Status
        """
        return cls(
            '/conversations/%s.json' % conversation.id,
            request_type=RequestPaginator.DELETE,
            singleton=True,
            session=session,
        )

    @classmethod
    def find_customer(cls, session, mailbox, customer):
        """Return conversations for a specific customer in a mailbox.

        Args:
            session (requests.Session): Authenticated requests Session.
            mailbox (helpscout.models.Mailbox): Mailbox to search.
            customer (helpscout.models.Customer): Customer to search for.

        Returns:
            RequestPaginator of Conversation: Conversations iterator.
        """
        return cls(
            '/mailboxes/%d/customers/%s/conversations.json' % (
                mailbox.id, customer.id,
            ),
            session=session,
        )

    @classmethod
    def find_user(cls, session, mailbox, user):
        """Return conversations for a specific user in a mailbox.

        Args:
            session (requests.Session): Authenticated requests Session.
            mailbox (helpscout.models.Mailbox): Mailbox to search.
            user (helpscout.models.User): User to search for.

        Returns:
            RequestPaginator of Conversation: Conversations iterator.
        """
        return cls(
            '/mailboxes/%d/users/%s/conversations.json' % (
                mailbox.id, user.id,
            ),
            session=session,
        )

    @classmethod
    def get(cls, session, conversation_id):
        """Return a specific conversation.

        Args:
            session (requests.Session): Authenticated requests Session.
            conversation_id (int): The ID of the conversation to get.

        Returns:
            Conversation: A conversation singleton, if existing.
            None: If no match for the ID.
        """
        return cls(
            '/conversations/%d.json' % conversation_id,
            singleton=True,
            session=session,
        )

    @classmethod
    def list(cls, session, mailbox):
        """Return conversations in a mailbox.

        Args:
            session (requests.Session): Authenticated requests Session.
            mailbox (helpscout.models.Mailbox): Mailbox to list.

        Returns:
            RequestPaginator of Conversation: Conversations iterator.
        """
        return cls(
            '/mailboxes/%d/conversations.json' % mailbox.id,
            session=session,
        )

    @classmethod
    def list_folder(cls, session, mailbox, folder):
        """Return conversations in a specific folder of a mailbox.

        Args:
            session (requests.Session): Authenticated requests Session.
            mailbox (helpscout.models.Mailbox): Mailbox that folder is in.
            folder (helpscout.models.Folder): Folder to list.

        Returns:
            RequestPaginator of Conversation: Conversations iterator.
        """
        return cls(
            '/mailboxes/%d/folders/%s/conversations.json' % (
                mailbox.id, folder.id,
            ),
            session=session,
        )

    @classmethod
    def search(cls, session, queries):
        """Search for a conversation given a domain.

        Args:
            session (requests.Session): Authenticated requests Session.
            queries (Domain | iter): The queries for the domain. If a
                ``Domain`` object is provided, it will simply be returned.
                Otherwise, a ``Domain`` object will be generated from the
                complex queries. In this case, the queries should conform
                to the interface in
                :func:`helpscout.domain.Domain.from_tuple`.

        Returns:
            RequestPaginator of SearchCustomer: SearchCustomer iterator.
        """
        domain = cls.get_search_domain(queries)
        cls(
            '/search/conversations.json',
            data={'query': str(domain)},
            session=session,
            object=SearchConversation,
        )

    @classmethod
    def update(cls, session, conversation, _reload=False):
        """Update a conversation.

        Args:
            session (requests.Session): Authenticated requests Session.
            conversation (Conversation): The conversation to be updated.
            _reload (bool, optional): Set this request parameter to ``True``
             to return the created conversation in the response.

        Returns:
            bool: Success status, if ``_reload`` is ``False``.
            Conversation: Freshly updated conversation, if ``_reload`` is
             ``True``.
        """
        data = {
            'conversation': conversation.to_api(),
            'reload': _reload,
        }
        return cls(
            '/conversations/%s.json' % conversation.id,
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
        )

    @classmethod
    def update_thread(cls, session, conversation, thread, _reload=False):
        """Update a thread.

        Args:
            session (requests.Session): Authenticated requests Session.
            conversation (Conversation): The conversation that the thread
             belongs to.
            thread (Thread): The thread to be updated.
            _reload (bool, optional): Set this request parameter to ``True``
             to return the created conversation in the response.

        Returns:
            bool: Success status, if ``_reload`` is ``False``.
            Thread: Freshly updated thread, if ``_reload`` is ``True``.
        """
        data = {
            'thread': thread.to_api(),
            'reload': _reload,
        }
        return cls(
            '/conversations/%s/threads/%d.json' % (
                conversation.id, thread.id,
            ),
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
            object=Thread,
        )
