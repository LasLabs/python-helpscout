# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel

from .option import Option


class CustomField(BaseModel):
    """This represents optional data that can defined for specific mailbox
    and filled when creating or updating a Conversation."""

    field_name = properties.String(
        'The name of the field; note that this may change if a field '
        'is renamed, but the ``id`` will not.',
        required=True,
    )
    field_type = properties.StringChoice(
        'Type of the field.',
        choices=['SINGLE_LINE',
                 'MULTI_LINE',
                 'DATA',
                 'NUMBER',
                 'DROPDOWN',
                 ],
        default='SINGLE_LINE',
        required=True,
    )
    required = properties.Bool(
        'Flag for UI to mark the field as required.',
    )
    order = properties.Integer(
        'Relative order of the custom field. Can be ``null`` or a number '
        'between ``0`` and ``255``.',
        min=0,
        max=255,
    )
    options = properties.List(
        'Field options',
        prop=Option,
    )
