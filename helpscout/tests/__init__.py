# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties


class BaseModel(properties.HasProperties):
    """This is the model that all other models inherit from.

    It provides some convenience functions, and the standard ``id`` property.
    """

    id = properties.Integer(
        'Unique identifier',
    )
