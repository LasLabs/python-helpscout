# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Source(BaseModel):

    type = properties.StringChoice(
        'The method from which this conversation (or thread) was created.',
        choices=['email', 'web', 'notification', 'emailfwd', 'api', 'chat'],
        default='api',
        required=True,
    )
    via = properties.StringChoice(
        'Indicates what type of entity this source represents (customer, '
        'user).',
        choices=['customer', 'user'],
    )
