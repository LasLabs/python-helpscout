# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Chat(BaseModel):
    """This represents a chat (IM) address."""

    value = properties.String(
        'Value',
        required=True,
    )
    type = properties.StringChoice(
        'Type',
        choices=['aim',
                 'gtalk',
                 'icq',
                 'xmpp',
                 'msn',
                 'skype',
                 'yahoo',
                 'qq',
                 'other',
                 ],
        default='other',
        required=True,
    )
