# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_conversation import BaseConversation


class SearchConversation(BaseConversation):
    """This represents a conversation as returned by search results."""

    mailbox_id = properties.Integer(
        'The ID of the mailbox this conversation is in.',
        required=True,
    )
    customer_name = properties.String(
        'Name of the customer this conversation is regarding.',
        required=True,
    )
    customer_email = properties.String(
        'Email address of the customer',
        required=True,
    )
    has_attachments = properties.Bool(
        '``True`` when the conversation has at least one attachment.',
    )
