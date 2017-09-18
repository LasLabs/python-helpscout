# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel

from .email import Email
from .mailbox_ref import MailboxRef
from .person import Person
from .source import Source
from .tag import Tag


class Conversation(BaseModel):
    """This represents a conversation."""

    type = properties.StringChoice(
        'The type of conversation.',
        choices=['email', 'chat', 'phone'],
        required=True,
    )
    folder_id = properties.Integer(
        'ID of the Mailbox Folder to which this conversation resides.',
        required=True,
    )
    is_draft = properties.Bool(
        'Is this a draft conversation?',
    )
    number = properties.Integer(
        'The conversation number displayed in the UI. This number can be used '
        'in combination with the id to construct a URL to the conversation on '
        'the Help Scout website. Example: '
        '``https://secure.helpscout.net/conversation/<id>/<number>/``',
        required=True,
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
    thread_count = properties.Integer(
        'This count represents the number of published threads found on the '
        'conversation (it does not include line items, drafts or threads held '
        'for review by Traffic Cop).',
        required=True,
    )
    status = properties.StringChoice(
        'Status of the conversation.',
        choices=['action', 'pending', 'closed', 'spam'],
        default='pending',
        required=True,
    )
    subject = properties.String(
        'Subject of conversation.',
    )
    preview = properties.String(
        'Conversation preview.',
    )
    created_by = properties.Instance(
        'The ``Person`` who created this conversation. The ``type`` property '
        'will specify whether it was created by a ``user`` or a ``customer``.',
        instance_class=Person,
    )
    created_at = properties.DateTime(
        'UTC time when this conversation was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when a user last modified this conversation.',
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
    cc = properties.List(
        'Emails that are CCd.',
        prop=Email,
    )
    bcc = properties.List(
        'Emails that are BCCd.',
        prop=Email,
    )
    tags = properties.List(
        'Tags for the conversation',
        prop=Tag,
    )
