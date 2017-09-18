# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Address(BaseModel):
    """This represents an address."""

    lines = properties.List(
        'Address line strings',
        prop=properties.String(
            'Address line string',
        ),
    )
    city = properties.String(
        'City',
        required=True,
    )
    state = properties.String(
        'State',
        required=True,
    )
    postal_code = properties.String(
        'Postal Code',
        required=True,
    )
    country = properties.String(
        'Country',
        required=True,
    )
    created_at = properties.DateTime(
        'UTC time when this address was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this address was modified.',
    )
