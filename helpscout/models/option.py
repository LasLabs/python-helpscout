# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Option(BaseModel):
    """This represents option for a custom field of type ``DROPDOWN``."""

    label = properties.String(
        'Label of the option.',
        required=True,
    )
    order = properties.Integer(
        'Relative order of the custom field. Can be ``null`` or a number '
        'between ``0`` and ``255``.',
        min=0,
        max=255,
    )
