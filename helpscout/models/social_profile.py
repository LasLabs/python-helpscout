# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class SocialProfile(BaseModel):

    value = properties.String(
        'Username',
        required=True,
    )
    type = properties.StringChoice(
        'Type of social profile.',
        choices=['twitter',
                 'facebook',
                 'linkedin',
                 'aboutme',
                 'google',
                 'googleplus',
                 'tungleme',
                 'quora',
                 'foursquare',
                 'youtube',
                 'flickr',
                 'other',
                 ],
        default='other',
        required=True,
    )
