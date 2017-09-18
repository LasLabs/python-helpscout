# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel

from .attachment import Attachment
from .email import Email
from .mailbox_ref import MailboxRef
from .person import Person
from .source import Source


class Thread(BaseModel):

    assigned_to = properties.Instance(
        'The Help Scout user assigned to this conversation.',
        instance_class=Person,
    )
    status = properties.StringChoice(
        'Status of the thread.',
        choices=['nochange', 'active', 'pending', 'closed', 'spam'],
    )
    created_at = properties.DateTime(
        'UTC time when this thread was created.',
    )
    opened_at = properties.DateTime(
        'UTC time when this thread was viewed by the customer. Only applies '
        'to threads with a ``type`` of message.',
    )
    created_by = properties.Instance(
        'The Person who created this thread. The ``type`` property will '
        'specify whether it was created by a ``user`` or a ``customer``.',
        instance_class=Person,
    )
    source = properties.Instance(
        'Origin of thread',
        instance_class=Source,
    )
    action_type = properties.StringChoice(
        'Describes an optional action associated with the line item.',
        choices=['movedFromMailbox',
                 'merged',
                 'imported',
                 'workflow',
                 'importedExternal',
                 'changedTicketCustomer',
                 'deletedTicket',
                 'restoreTicket',
                 ],
    )
    action_source_id = properties.Integer(
        'Associated with the ``action_type`` property. \n'
        '* If ``action_type`` is ``movedFromMailbox``, this will be the id '
        '  of the mailbox the conversation was moved from. \n'
        '* If ``action_type`` is ``merged``, this will be the id of the '
        '  original conversation. \n'
        '* If ``action_type`` is ``imported``, this will be null. \n'
        '* If ``action_type`` is ``workflow``, this will be the id of the '
        '  workflow that was run.',
    )
    from_mailbox = properties.Instance(
        'If the conversation was moved, this represents the MailboxRef from '
        'which it was moved.',
        instance_class=MailboxRef,
    )
    type = properties.StringChoice(
        'The type of thread. \n'
        'A ``lineitem`` represents a change of state on the conversation. '
        'This could include, but not limited to, the conversation was '
        'assigned, the status changed, the conversation was moved from one '
        'mailbox to another, etc. A line item won\'t have a body, to/cc/bcc '
        'lists, or attachments. \n'
        'When a conversation is forwarded, a new conversation is created to '
        'represent the forwarded conversation. \n'
        '``forwardparent ``is the type set on the thread of the original '
        'conversation that initiated the forward event. \n'
        '``forwardchild`` is the type set on the first thread of the new '
        'forwarded conversation.',
        choices=['lineitem',
                 'note',
                 'message',
                 'chat',
                 'customer',
                 'forwardparent',
                 'forwardchild',
                 'phone',
                 ],
    )
    state = properties.StringChoice(
        'The state of the thread. \n'
        'A state of ``underreview`` means the thread has been stopped by '
        'Traffic Cop and is waiting to be confirmed (or discarded) by the '
        'person that created the thread. \n'
        'A state of ``hidden`` means the thread was hidden (or removed) from '
        'customer-facing emails.',
        choices=['pubished', 'draft', 'underreview', 'hidden'],
    )
    customer = properties.Instance(
        'If thread type is ``message``, this is the customer associated with '
        'the conversation. \n'
        'If thread type is ``customer``, this is the the customer who '
        'initiated the thread.',
        instance_class=Person,
    )
    body = properties.String(
        'Body text',
    )
    to = properties.List(
        'Email to',
        prop=Email,
    )
    cc = properties.List(
        'CC to',
        prop=Email,
    )
    bcc = properties.List(
        'BCC to',
        prop=Email,
    )
    attachments = properties.List(
        'Attachments',
        prop=Attachment,
    )
    saved_reply_id = properties.Integer(
        'ID of Saved reply that was used to create this Thread.',
    )
    created_by_customer = properties.Bool(
        'Equivalent to ``created_by.type == "customer"``.',
    )
