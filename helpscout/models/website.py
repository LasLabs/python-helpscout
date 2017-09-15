# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Website(BaseModel):

    value = properties.String(
        'URI',
        required=True,
    )
