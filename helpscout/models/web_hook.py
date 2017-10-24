# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel
from .web_hook_event import event_type


class WebHook(BaseModel):

    url = properties.String(
        'The callback URL where Help Scout will post your webhook events. '
        'This is the script or location where you\'ll handle the data '
        'received from Help Scout.',
        required=True,
    )
    secret_key = properties.String(
        'A randomly-generated (by you) string of 40 characters or less used '
        'to create signatures for each webhook method. Help Scout uses this '
        'secret key to generate a signature for each webhook message. When '
        'the message is received at your callback URL, you can calculate a '
        'signature and compare to the one Help Scout sends. If the '
        'signatures match, you know it\'s from Help Scout.',
        required=True,
    )
    events = properties.List(
        'The events to subscribe to.',
        prop=event_type,
    )
