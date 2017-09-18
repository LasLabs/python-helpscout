# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel

from .user import User


class Folder(BaseModel):

    name = properties.String(
        'Folder name',
        required=True,
    )
    type = properties.StringChoice(
        'The type of folder.',
        choices=['unassigned',
                 'mytickets',
                 'needsattention',
                 'drafts',
                 'assigned',
                 'closed',
                 'spam',
                 ],
        default='drafts',
        required=True,
    )
    user_id = properties.Instance(
        'If the folder type is ``MyTickets``, this represents the Help Scout '
        'user to which this folder belongs. Otherwise it is empty.',
        instance_class=User,
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
