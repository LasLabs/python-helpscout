# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class BaseConversation(BaseModel):
    """This represents a basic conversation, meant to be subclassed."""

    number = properties.Integer(
        'The conversation number displayed in the UI. This number can be used '
        'in combination with the id to construct a URI to the conversation on '
        'the Help Scout website. Example: '
        '``https://secure.helpscout.net/conversation/<id>/<number>/``',
        required=True,
    )
    subject = properties.String(
        'The subject of the conversation.',
        required=True,
    )
    status = properties.StringChoice(
        'Status of the conversation.',
        choices=['active', 'pending', 'closed', 'spam'],
        default='pending',
        required=True,
    )
    thread_count = properties.Integer(
        'This count represents the number of published threads found on the '
        'conversation (it does not include line items, drafts or threads held '
        'for review by Traffic Cop).',
        required=True,
    )
    preview = properties.String(
        'Conversation preview.',
    )
    modified_at = properties.DateTime(
        'UTC time when a user last modified this conversation.',
    )
