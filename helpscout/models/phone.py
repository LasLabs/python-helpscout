# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Phone(BaseModel):

    value = properties.String(
        'Phone Number',
        required=True,
    )
    location = properties.StringChoice(
        'Location for this phone number.',
        choices=['home',
                 'fax',
                 'mobile',
                 'pager',
                 'work',
                 'other',
                 ],
        default='other',
        required=True,
    )
