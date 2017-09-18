# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Email(BaseModel):

    value = properties.String(
        'Email Address',
        required=True,
    )
    location = properties.StringChoice(
        'Location for this email address.',
        choices=['home', 'work', 'other'],
        default='other',
        required=True,
    )
