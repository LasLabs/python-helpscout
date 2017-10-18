# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Attachment(BaseModel):

    hash = properties.String(
        'Unique hash.',
        required=True,
    )
    mime_type = properties.String(
        'Mime Type',
    )
    filename = properties.String(
        'File Name',
        required=True,
    )
    size = properties.Integer(
        'Size of the attachment in bytes.',
    )
    width = properties.Integer(
        'Image width',
    )
    height = properties.Integer(
        'Image height',
    )
    url = properties.String(
        'Public-facing url where attachment can be downloaded.',
    )
