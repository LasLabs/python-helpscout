# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel

EVENT_CHOICES = {
    'convo.assigned': 'Conversation was assigned.',
    'convo.created': 'Conversation was created.',
    'convo.deleted': 'Conversation was deleted.',
    'convo.merged': 'Conversation was merged.',
    'convo.moved': 'Conversation was moved.',
    'convo.status': 'Conversation status was updated.',
    'convo.tags': 'Conversation tags were updated.',
    'convo.customer.reply.created': 'The customer replied to the '
                                    'conversation.',
    'convo.agent.reply.created': 'An agent replied to the conversation.',
    'convo.note.created': 'A note was added to the conversation.',
    'customer.created': 'A customer was created.',
    'satisfaction.ratings': 'A rating was received.',
}

event_type = properties.StringChoice(
    'The event type that this object represents.',
    required=True,
    choices=sorted(EVENT_CHOICES.keys()),
    descriptions=EVENT_CHOICES,
)


class WebHookEvent(BaseModel):

    event_type = event_type
    record = properties.Instance(
        'The parsed data record that was received in the request.',
        instance_class=BaseModel,
        required=True,
    )
