# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon

from ..apis.conversations import Conversations

from ..models.search_conversation import SearchConversation
from ..models.thread import Thread


class TestApiConversations(ApiCommon):

    def test_create(self):
        data = {
            'conversation': self.mock_record.to_api(),
            'imported': True,
            'auto_reply': True,
            'reload': True,
        }
        args = [self.mock_record, True, True]
        self._test_method(
            Conversations, 'create', args, '/conversations.json',
            data, 'post', True,
        )

    def test_create_thread(self):
        thread = self.mock_record.thread
        data = {
            'thread': thread.to_api(),
            'imported': True,
            'reload': True,
        }
        args = [self.mock_record, self.mock_record.thread, True]
        uri = '/conversations/%d.json' % self.mock_record.id
        self._test_method(
            Conversations, 'create_thread', args, uri,
            data, 'post', True, Thread,
        )

    def test_delete(self):
        uri = '/conversations/%s.json' % self.mock_record.id
        self._test_method(
            Conversations, 'delete', [self.mock_record], uri,
            None, 'delete', False,
        )

    def test_find_customer(self):
        customer = self.mock_record.customer
        customer.id = 9876
        uri = '/mailboxes/%d/customers/%s/conversations.json' % (
            self.mock_record.id, customer.id,
        )
        args = [self.mock_record, customer]
        self._test_method(
            Conversations, 'find_customer', args, uri,
        )

    def test_find_user(self):
        user = self.mock_record.user
        user.id = 9876
        uri = '/mailboxes/%d/users/%s/conversations.json' % (
            self.mock_record.id, user.id,
        )
        args = [self.mock_record, user]
        self._test_method(
            Conversations, 'find_user', args, uri,
        )

    def test_get(self):
        uri = '/conversations/%s.json' % self.mock_record.id
        self._test_method(
            Conversations, 'get', [self.mock_record.id], uri,
            singleton=True,
        )

    def test_list(self):
        uri = '/mailboxes/%d/conversations.json' % self.mock_record.id
        self._test_method(
            Conversations, 'list', [self.mock_record], uri,
        )

    def test_list_folder(self):
        folder = self.mock_record.folder
        folder.id = 9876
        uri = '/mailboxes/%d/folders/%d/conversations.json' % (
            self.mock_record.id, folder.id,
        )
        self._test_method(
            Conversations, 'list_folder', [self.mock_record, folder], uri,
        )

    def test_search(self):
        data = {'query': "()"}
        self._test_method(
            Conversations, 'search', [[]], '/search/conversations.json', data,
            out_type=SearchConversation,
        )

    def test_update(self):
        uri = '/conversations/%s.json' % self.mock_record.id
        self._test_method(
            Conversations, 'update', [self.mock_record], uri, self.mock_record,
            singleton=True,
        )

    def test_update_thread(self):
        thread = self.mock_record.thread
        thread.id = 9876
        uri = '/conversations/%s/threads/%d.json' % (
            self.mock_record.id, thread.id,
        )
        self._test_method(
            Conversations, 'update_thread', [self.mock_record, thread], uri,
            thread, singleton=True, out_type=Thread,
        )
