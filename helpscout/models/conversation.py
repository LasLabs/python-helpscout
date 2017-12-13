# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_conversation import BaseConversation

from .mailbox_ref import MailboxRef
from .person import Person
from .source import Source
from .thread import Thread


class Conversation(BaseConversation):
    """This represents a full conversation result."""

    type = properties.StringChoice(
        'The type of conversation.',
        choices=['email', 'chat', 'phone', 'spam'],
        required=True,
    )
    folder_id = properties.Integer(
        'ID of the Mailbox Folder to which this conversation resides.',
        required=True,
    )
    is_draft = properties.Bool(
        'Is this a draft conversation? This property duplicates ``draft``, '
        'but both are received in API responses at the same time so neither '
        'can be considered "deprecated".',
    )
    draft = properties.Bool(
        'Is this a draft conversation? This property duplicates '
        '``is_draft``, but both are received in API responses at the same '
        'time so neither can be considered "deprecated".',
    )
    owner = properties.Instance(
        'The Help Scout user who is currently assigned to this conversation.',
        instance_class=Person,
        required=True,
    )
    mailbox = properties.Instance(
        'The mailbox to which this conversation belongs.',
        instance_class=MailboxRef,
        required=True,
    )
    customer = properties.Instance(
        'The customer who this conversation is associated with.',
        instance_class=Person,
        required=True,
    )
    created_by = properties.Instance(
        'The ``Person`` who created this conversation. The ``type`` property '
        'will specify whether it was created by a ``user`` or a ``customer``.',
        instance_class=Person,
    )
    created_by_type = properties.String(
        'The type of user that created this conversation.',
    )
    created_at = properties.DateTime(
        'UTC time when this conversation was created.',
    )
    closed_at = properties.DateTime(
        'UTC time when this conversation was closed. Null if not closed.',
    )
    closed_by = properties.Instance(
        'The Help Scout user who closed this conversation.',
        instance_class=Person,
    )
    source = properties.Instance(
        'Specifies the method in which this conversation was created.',
        instance_class=Source,
    )
    threads = properties.List(
        'Threads associated with the conversation.',
        prop=Thread,
    )
    cc = properties.List(
        'Emails that are CCd.',
        prop=properties.String(
            'Email Address',
        ),
    )
    bcc = properties.List(
        'Emails that are BCCd.',
        prop=properties.String(
            'Email Address',
        ),
    )
    tags = properties.List(
        'Tags for the conversation',
        prop=properties.String('Tag Name'),
    )
    spam = properties.Bool(
        'If this conversation is marked as SPAM.',
    )
    locked = properties.Bool(
        'If this conversation is locked from editing.'
    )
    user_modified_at = properties.DateTime(
        'Last time that this conversation was edited by a user.',
    )
