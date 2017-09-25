# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel
from ..models import Conversation, Customer, Rating


class WebHookEvent(properties.HasProperties):
    """``WebHookEvent`` represents an authenticated web hook request.

    Note that this object is meant to represent an authenticated Web Hook,
    and therefore is completely naive of all things authentication. Any
    request authentication/validation should happen in the ``WebHook``.
    """

    # Map the event prefixes to their corresponding data models.
    EVENT_PREFIX_TO_MODEL = {
        'convo': Conversation,
        'customer': Customer,
        'satisfaction': Rating,
    }

    event_type = properties.String(
        'The event type that this object represents.',
        required=True,
    )
    record = properties.Instance(
        'The parsed data record that was received in the request.',
        instance_class=BaseModel,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        """Parse raw record data if required.

        Args:
            record (dict or BaseModel): The record data that was received for
                the request. If it is a ``dict``, the data will be parsed
                using the proper model's ``from_api`` method.
        """
        if isinstance(kwargs.get('record'), dict):
            prefix, _ = kwargs['event_type'].split('.', 1)
            model = self.EVENT_PREFIX_TO_MODEL[prefix]
            kwargs['record'] = model.from_api(**kwargs['record'])
        super(WebHookEvent, self).__init__(*args, **kwargs)
