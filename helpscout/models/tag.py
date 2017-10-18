# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Tag(BaseModel):

    name = properties.String(
        'The tag value.',
        required=True,
    )
    slug = properties.String(
        'Slugified version of the tag value.',
    )
    count = properties.Integer(
        'The number of times the tag is used.',
    )
    color = properties.Color(
        'The tag color.',
        required=True,
    )
    created_at = properties.DateTime(
        'UTC time when this tag was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this tag was modified.',
    )
