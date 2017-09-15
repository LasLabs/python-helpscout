# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Field(BaseModel):
    """The field object represents a user's response to a custom field
       in the context of a single conversation."""

    field_id = properties.Integer(
        'The field definition identifier; note that multiple conversations '
        'will each have values for the same field identifier.',
    )
    name = properties.String(
        'The name of the field; note that this may change if a field is '
        'renamed, but the ``field_id`` will not.',
        required=True,
    )
    value = properties.String(
        'The value the user specified for the field.',
    )
    type = properties.StringChoice(
        'Type of the custom field.',
        choices=['SINGLE_LINE',
                 'MULTI_LINE',
                 'DATE',
                 'NUMBER',
                 'DROPDOWN',
                 ],
    )
    label = properties.String(
        'String representation of the custom field\'s value. Unlike '
        '``value`` it contains the actual dropdown option value for '
        '``DROPDOWN`` custom field.',
    )
