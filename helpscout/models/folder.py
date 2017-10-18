# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Folder(BaseModel):

    name = properties.String(
        'Folder name',
        required=True,
    )
    type = properties.StringChoice(
        'The type of folder.',
        choices=['needsattention',
                 'drafts',
                 'assigned',
                 'open',
                 'closed',
                 'spam',
                 'mine',
                 ],
        default='drafts',
        required=True,
    )
    user_id = properties.Integer(
        'If the folder type is ``MyTickets``, this represents the Help Scout '
        'user to which this folder belongs. Otherwise it is empty.',
    )
    total_count = properties.Integer(
        'Total number of conversations in this folder.',
    )
    active_count = properties.Integer(
        'Total number of conversations in this folder that are in an active '
        'state (vs pending).',
    )
    modified_at = properties.DateTime(
        'UTC time when this folder was modified.',
    )
