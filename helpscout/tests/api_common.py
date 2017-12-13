# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from os.path import dirname, join

from vcr import VCR

from .. import HelpScout

from .. import BaseModel

from ..models.attachment import Attachment
from ..models.customer import Customer
from ..models.conversation import Conversation
from ..models.folder import Folder
from ..models.mailbox_ref import MailboxRef
from ..models.person import Person
from ..models.thread import Thread
from ..models.user import User


recorder = VCR(
    record_mode='once',
    cassette_library_dir=join(dirname(__file__), 'fixtures/cassettes'),
    path_transformer=VCR.ensure_suffix('.yml'),
    filter_headers=['Authorization'],
)


class ApiCommon(unittest.TestCase):

    # This should be set to the API endpoint object in children
    __endpoint__ = None

    def setUp(self):
        super(ApiCommon, self).setUp()
        self.api = HelpScout(
            '06501c1e20bcb8a489f428b3b6a08c6bffaef190',
        )
        self.mock_record = mock.MagicMock()
        self.mock_class = mock.MagicMock()
        self.mock_session = mock.MagicMock()
        self.mock_record.id = 1234

    def _get_user(self, strip_id=False):
        """Return a User object."""
        user = User.deserialize({
            'first_name': u'Dave',
            'last_name': u'Lasley',
            'created_at': '2017-08-25T20:01:06Z',
            'modified_at': '2017-12-13T19:47:35Z',
            'emails': [],
            'id': 218639,
            'role': 'owner',
            'full_name': u'Dave Lasley',
            'timezone': u'America/New_York',
            'type': 'user',
            'email': u'support@example.com',
            'photo_url': u'https://d33v4339jhl8k0.cloudfront.net/'
                         u'users/218639.95870.jpg',
        })
        return self._strip_id(user, strip_id)

    def _get_person_user(self, strip_id=False):
        """Return a Person object for a user."""
        user = Person.deserialize({
            'first_name': u'Dave',
            'last_name': u'Lasley',
            'emails': [],
            'id': 218639,
            'full_name': u'Dave Lasley',
            'type': 'user',
            'email': u'support@example.com',
            'photo_url': u'https://d33v4339jhl8k0.cloudfront.net/'
                         u'users/218639.95870.jpg',
        })
        return self._strip_id(user, strip_id)

    def _get_customer(self, strip_id=False):
        """Return a Customer object."""
        customer = Customer.deserialize({
            'chats': [],
            'first_name': u'Test',
            'last_name': u'User',
            'phones': [],
            'created_at': '2017-09-23T20:12:43Z',
            'modified_at': '2017-12-13T22:39:59Z',
            'websites': [],
            'emails': [],
            'full_name': u'Test User',
            'gender': 'unknown',
            'id': 144228647,
            'organization': u'Test Company',
            'type': 'user',
            'social_profiles': [],
            'job_title': u'CEO',
        })
        return self._strip_id(customer, strip_id)

    def _get_person_customer(self, strip_id=False):
        """Return a Person object for a customer."""
        customer = Person.deserialize({
            'first_name': u'Test',
            'last_name': u'User',
            'email': u'test@example.com',
            'phone': u'1234567890',
            'id': 144228647,
            'type': 'customer',
            'emails': [u'test@example.com'],
            'photo_url': u'',
        })
        return self._strip_id(customer, strip_id)

    def _get_mailbox_ref(self, strip_id=False):
        """Return a MailboxRef object."""
        mailbox_ref = MailboxRef.deserialize({
            'id': 122867,
            'name': u'Support',
        })
        return self._strip_id(mailbox_ref, strip_id)

    def _get_thread(self, strip_id=False):
        thread = Thread.deserialize({
            'status': 'active',
            'body': u'<p>Test conversation.</p>',
            'created_by_customer': False,
            'attachments': [],
            'to': [],
            'cc': [],
            'created_at': '2017-12-07T21:08:20Z',
            'created_by': self._get_person_user().serialize(),
            'bcc': [],
            'customer': self._get_person_customer().serialize(),
            'state': 'published',
            'source': {
                'via': 'user',
                'type': 'api',
            },
            'type': 'note',
            'id': 1310543489,
        })
        return self._strip_id(thread, strip_id)

    def _get_conversation(self, strip_id=False):
        """Return a Conversation object."""
        conversation = Conversation.deserialize({
            'status': 'pending',
            'customer': self._get_person_customer().serialize(),
            'preview': u'Conversation exported from Odoo.',
            'tags': [],
            'thread_count': 1,
            'type': 'email',
            'created_at': '2017-12-07T21:08:20Z',
            'number': 162,
            'created_by': self._get_person_user().serialize(),
            'mailbox': self._get_mailbox_ref().serialize(),
            'source': {
                'via': 'user',
                'type': 'api',
            },
            'threads': [
                self._get_thread(strip_id=strip_id).serialize(),
            ],
            'folder_id': 1601748,
            'owner': self._get_person_user().serialize(),
            'bcc': [],
            'is_draft': False,
            'id': 448848612,
            'cc': [],
            'subject': u'Celebrate successful conversation.',
        })
        return self._strip_id(conversation, strip_id)

    def _get_folder(self):
        return Folder.deserialize({
            'user_id': self._get_user().id,
            'name': u'Mine',
            'total_count': 2,
            'modified_at': '2017-12-14T00:28:40Z',
            'active_count': 1,
            'type': 'mine',
            'id': 1601748,
        })

    def _get_team(self, strip_id=False):
        team = Person.deserialize({
            'first_name': u'Test Team',
            'last_name': u'',
            'created_at': '2017-12-14T01:18:46Z',
            'modified_at': '2017-12-14T01:18:51Z',
            'emails': [],
            'full_name': u'Test Team ',
            'id': 245377,
            'type': 'team',
            'email': u'',
        })
        return self._strip_id(team, strip_id)

    def _new_attachment(self):
        return Attachment(
            raw_data='Test String',
            file_name='test.txt',
            mime_type='text/plain',
        )

    def _strip_id(self, obj, do_strip):
        if do_strip:
            obj.id = False
        return obj

    def _test_create(self, record):
        """Generic create API endpoint test helper."""
        response = self.__endpoint__.create(record)
        self.assertIsInstance(response, record.__class__)
        self.assertTrue(response.id)
        return response

    def _test_get(self, record):
        """Generic get API endpoint test helper."""
        result = self.__endpoint__.get(record.id)
        self.assertEqual(result.id, record.id)
        return result

    def _test_delete(self, record):
        """Generic delete API endpoint test helper."""
        record = self.__endpoint__.create(record)
        self.assertTrue(self.__endpoint__.get(record.id))
        self.assertIsNone(self.__endpoint__.delete(record))
        self.assertFalse(self.__endpoint__.get(record.id))

    def _test_list(self, *args):
        """Generic list API endpoint test helper."""
        self._assert_results(
            self.__endpoint__.list(*args),
            lambda r: isinstance(r, BaseModel),
        )

    def _test_search(self, record):
        """Generic search API endpoint test helper."""
        query = [('id', record.id)]
        result_ids = [r.id for r in self.__endpoint__.search(query)]
        self.assertIn(record.id, result_ids)

    def _test_update(self, record, update_attr, update_val):
        """Generic update API endpoint test helper."""
        record = self.__endpoint__.create(record)
        setattr(record, update_attr, update_val)
        self.__endpoint__.update(record)
        self.assertEqual(
            getattr(self.__endpoint__.get(record.id), update_attr),
            update_val,
        )

    def _assert_results(self, result_iterator, assert_method=None):
        result_counter = 0
        for result in result_iterator:
            if assert_method is not None:
                self.assertTrue(assert_method(result))
            result_counter += 1
        self.assertTrue(result_counter)
