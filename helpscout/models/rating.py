# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel

from .customer import Customer
from .mailbox_ref import MailboxRef


class Rating(BaseModel):

    customer = properties.Instance(
        'Partial customer object.',
        instance_class=Customer,
        required=True,
    )
    ticket_id = properties.Integer(
        'Ticket ID',
        required=True,
    )
    thread_id = properties.Integer(
        'Thread ID',
        required=True,
    )
    mailbox = properties.Instance(
        'Reference to the mailbox that the conversation belongs to.',
        instance_class=MailboxRef,
        required=True,
    )
    rating = properties.StringChoice(
        'Satisfaction rating.',
        choices=['Great', 'Okay', 'Bad'],
        required=True,
    )
    comments = properties.String(
        'Additional comments',
    )
    created_at = properties.DateTime(
        'UTC time when this rating was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this rating was modified.',
    )
