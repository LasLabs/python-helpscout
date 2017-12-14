# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon, recorder

from ..models.attachment import Attachment


class TestApisConversations(ApiCommon):
    """Tests the Conversations API endpoint."""

    def setUp(self):
        super(TestApisConversations, self).setUp()
        self.__endpoint__ = self.api.Conversations

    def _test_attachment(self):
        attachment = self.api.Conversations.create_attachment(
            self._new_attachment(),
        )
        self.assertIsInstance(attachment, Attachment)
        self.assertTrue(attachment.hash)
        return attachment

    def _conversation_with_attachment(self, conversation, thread):
        thread['attachments'] = [self._test_attachment()]
        conversation = self.api.Conversations.create_thread(
            conversation, thread,
        )
        return conversation, conversation['threads'][0]['attachments'][0]

    @recorder.use_cassette()
    def test_apis_conversations_create(self):
        """It should create and return a Conversation."""
        self._test_create(self._get_conversation(strip_id=True))

    @recorder.use_cassette()
    def test_apis_conversations_create_attachment(self):
        """It should create and return the Attachment."""
        self._test_attachment()

    @recorder.use_cassette()
    def test_apis_conversations_create_thread(self):
        """It should create the thread and return the conversation."""
        conversation = self._test_create(
            self._get_conversation(strip_id=True),
        )
        thread_count = conversation.thread_count
        thread = self._get_thread(strip_id=True)
        conversation = self.api.Conversations.create_thread(
            conversation, thread,
        )
        self.assertEqual(
            len(conversation.threads), thread_count + 1,
        )

    @recorder.use_cassette()
    def test_apis_conversations_get(self):
        """It should return the conversation."""
        self._test_get(self._get_conversation())

    @recorder.use_cassette()
    def test_apis_conversations_delete(self):
        """It should delete the conversation."""
        self._test_delete(self._get_conversation(strip_id=True))

    @recorder.use_cassette()
    def test_apis_conversations_list(self):
        """It should list the conversations in the mailbox."""
        mailbox = self._get_mailbox_ref()
        self._test_list(mailbox)

    @recorder.use_cassette()
    def test_apis_conversations_search(self):
        """It should search for and return the conversation."""
        self._test_search(self._get_conversation())

    @recorder.use_cassette()
    def test_apis_conversations_update(self):
        """It should update the conversation."""
        self._test_update(
            self._get_conversation(strip_id=True),
            'subject',
            'A new subject',
        )

    @recorder.use_cassette()
    def test_apis_conversations_find_customer(self):
        """It should only return conversations for the customer."""
        mailbox = self._get_mailbox_ref()
        customer = self._get_customer()
        self._assert_results(
            self.api.Conversations.find_customer(mailbox, customer),
            lambda result: result.customer.id == customer.id,
        )

    @recorder.use_cassette()
    def test_apis_conversations_find_user(self):
        """It should only return conversations for the user."""
        mailbox = self._get_mailbox_ref()
        user = self._get_user()
        self._assert_results(
            self.api.Conversations.find_user(mailbox, user),
            lambda result: result.owner.id == user.id,
        )

    @recorder.use_cassette()
    def test_apis_conversations_get_attachment_data(self):
        """It should return the proper attachment."""
        _, attachment = self._conversation_with_attachment(
            self._get_conversation(),
            self._get_thread(strip_id=True),
        )
        response = self.api.Conversations.get_attachment_data(attachment.id)
        self.assertEqual(response.raw_data, self._new_attachment().raw_data)

    @recorder.use_cassette()
    def test_apis_conversations_delete_attachment(self):
        """It should return None after a success."""
        _, attachment = self._conversation_with_attachment(
            self._get_conversation(),
            self._get_thread(strip_id=True),
        )
        self.assertIsNone(
            self.api.Conversations.delete_attachment(attachment),
        )

    @recorder.use_cassette()
    def test_apis_conversations_list_folder(self):
        """It should return conversations specific to a folder."""
        mailbox = self._get_mailbox_ref()
        folder = self._get_folder()
        self._assert_results(
            self.api.Conversations.list_folder(mailbox, folder),
            lambda record: record.folder_id == folder.id,
        )

    @recorder.use_cassette()
    def test_apis_conversations_update_thread(self):
        """It should update the thread."""
        conversation, _ = self._conversation_with_attachment(
            self._get_conversation(),
            self._get_thread(strip_id=True),
        )
        thread = conversation['threads'][0]
        thread.body = 'expect'
        conversation = self.api.Conversations.update_thread(
            conversation, thread,
        )
        self.assertEqual(
            conversation['threads'][0].body, 'expect',
        )
