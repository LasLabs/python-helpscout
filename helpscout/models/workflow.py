# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Workflow(BaseModel):

    mailbox_id = properties.Integer(
        'The mailbox ID that this workflow is associated with.',
        required=True,
    )
    type = properties.StringChoice(
        'The type of workflow.',
        choices=['automatic', 'manual'],
        default='manual',
        required=True,
    )
    status = properties.StringChoice(
        'The status of the workflow.',
        choices=['active', 'inactive', 'invalid'],
        default='invalid',
        required=True,
    )
    order = properties.Integer(
        'The order of the workflow.',
        default=1,
        required=True,
    )
    name = properties.String(
        'Workflow name.',
        required=True,
    )
    created_at = properties.DateTime(
        'UTC time when this workflow was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this workflow was modified.',
    )
