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
      (:func:`helpscout.apis.conversations.Conversations.list`)
    * `Search Conversations
      <http://developer.helpscout.net/help-desk-api/search/conversations/>`_
      (:func:`helpscout.apis.conversations.Conversations.search`)
    * `Get Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/get/>`_
      (:func:`helpscout.apis.conversations.Conversations.get`)
    * `Create Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/create/>`_
      (:func:`helpscout.apis.conversations.Conversations.create`)
    * `Update Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/update/>`_
      (:func:`helpscout.apis.conversations.Conversations.update`)
    * `Delete Conversation
      <http://developer.helpscout.net/help-desk-api/conversations/delete/>`_
      (:func:`helpscout.apis.conversations.Conversations.delete`)
    * `Create Thread
      <http://developer.helpscout.net/help-desk-api/conversations/
      create-thread/>`_
      (:func:`helpscout.apis.conversations.Conversations.create_thread`)
    * `Update Thread
      <http://developer.helpscout.net/help-desk-api/conversations/
      update-thread/>`_
      (:func:`helpscout.apis.conversations.Conversations.update_thread`)
    """

    __object__ = Conversation

    @classmethod
    def create(cls, session, conversation, imported=False, auto_reply=False):
        """Create a conversation.

        Please note that conversation cannot be created with more than 100
        threads, if attempted the API will respond with HTTP 412.

        Args:
            session (requests.sessions.Session): Authenticated session.
            conversation (helpscout.models.Conversation): The conversation
             to be created.
            imported (bool, optional): The ``imported`` request parameter
             enables conversations to be created for historical purposes (i.e.
             if moving from a different platform, you can import your
             history). When ``imported`` is set to ``True``, no outgoing
             emails or notifications will be generated.
            auto_reply (bool): The ``auto_reply`` request parameter enables
             auto replies to be sent when a conversation is created via the
             API. When ``auto_reply`` is set to ``True``, an auto reply will
             be sent as long as there is at least one ``customer`` thread in
             the conversation.

        Returns:
            helpscout.models.Conversation: Newly created conversation.
        """
        data = {
            'conversation': conversation.to_api(),
            'imported': imported,
            'auto_reply': auto_reply,
            'reload': True,
        }
        return cls(
            '/conversations.json',
            data=data,
            request_type=RequestPaginator.POST,
            singleton=True,
            session=session,
        )

    @classmethod
    def create_thread(cls, session, conversation, thread, imported=False):
        """Create a conversation thread.

        Please note that threads cannot be added to conversations with 100
        threads (or more), if attempted the API will respond with HTTP 412.

        Args:
            conversation (helpscout.models.Conversation): The conversation
             that the thread is being added to.
            session (requests.sessions.Session): Authenticated session.
            thread (helpscout.models.Thread): The thread to be created.
            imported (bool, optional): The ``imported`` request parameter
             enables conversations to be created for historical purposes (i.e.
             if moving from a different platform, you can import your
             history). When ``imported`` is set to ``True``, no outgoing
             emails or notifications will be generated.

        Returns:
            helpscout.models.Thread: Newly created thread.
        """
        data = {
            'thread': thread.to_api(),
            'imported': imported,
            'reload': True,
        }
        return cls(
            '/conversations/%s.json' % conversation.id,
            data=data,
            request_type=RequestPaginator.POST,
            singleton=True,
            session=session,
            out_type=Thread,
        )

    @classmethod
    def delete(cls, session, conversation):
        """Delete a conversation.

        Args:
            session (requests.sessions.Session): Authenticated session.
            conversation (helpscout.models.Conversation): The conversation to
                be deleted.

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
            session (requests.sessions.Session): Authenticated session.
            mailbox (helpscout.models.Mailbox): Mailbox to search.
            customer (helpscout.models.Customer): Customer to search for.

        Returns:
            RequestPaginator(output_type=helpscout.models.Conversation):
                Conversations iterator.
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
            session (requests.sessions.Session): Authenticated session.
            mailbox (helpscout.models.Mailbox): Mailbox to search.
            user (helpscout.models.User): User to search for.

        Returns:
            RequestPaginator(output_type=helpscout.models.Conversation):
                Conversations iterator.
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
            session (requests.sessions.Session): Authenticated session.
            conversation_id (int): The ID of the conversation to get.

        Returns:
            helpscout.models.Conversation: A conversation singleton, if
                existing. Otherwise ``None``.
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
            session (requests.sessions.Session): Authenticated session.
            mailbox (helpscout.models.Mailbox): Mailbox to list.

        Returns:
            RequestPaginator(output_type=helpscout.models.Conversation):
                Conversations iterator.
        """
        return cls(
            '/mailboxes/%d/conversations.json' % mailbox.id,
            session=session,
        )

    @classmethod
    def list_folder(cls, session, mailbox, folder):
        """Return conversations in a specific folder of a mailbox.

        Args:
            session (requests.sessions.Session): Authenticated session.
            mailbox (helpscout.models.Mailbox): Mailbox that folder is in.
            folder (helpscout.models.Folder): Folder to list.

        Returns:
            RequestPaginator(output_type=helpscout.models.Conversation):
                Conversations iterator.
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
            session (requests.sessions.Session): Authenticated session.
            queries (helpscout.models.Domain or iter): The queries for the
                domain. If a ``Domain`` object is provided, it will simply be
                returned. Otherwise, a ``Domain`` object will be generated
                from the complex queries. In this case, the queries should
                conform to the interface in
                :func:`helpscout.domain.Domain.from_tuple`.

        Returns:
            RequestPaginator(output_type=helpscout.models.SearchCustomer):
                SearchCustomer iterator.
        """
        domain = cls.get_search_domain(queries)
        return cls(
            '/search/conversations.json',
            data={'query': str(domain)},
            session=session,
            out_type=SearchConversation,
        )

    @classmethod
    def update(cls, session, conversation):
        """Update a conversation.

        Args:
            session (requests.sessions.Session): Authenticated session.
            conversation (helpscout.models.Conversation): The conversation to
                be updated.

        Returns:
            helpscout.models.Conversation: Freshly updated conversation.
        """
        data = conversation.to_api()
        data['reload'] = True
        return cls(
            '/conversations/%s.json' % conversation.id,
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
        )

    @classmethod
    def update_thread(cls, session, conversation, thread):
        """Update a thread.

        Args:
            session (requests.sessions.Session): Authenticated session.
            conversation (helpscout.models.Conversation): The conversation
                that the thread belongs to.
            thread (helpscout.models.Thread): The thread to be updated.

        Returns:
            helpscout.models.Thread: Freshly updated thread.
        """
        data = thread.to_api()
        data['reload'] = True
        return cls(
            '/conversations/%s/threads/%d.json' % (
                conversation.id, thread.id,
            ),
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
            out_type=Thread,
        )
