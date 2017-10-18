# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .person import Person


class User(Person):

    role = properties.StringChoice(
        'Role of this user.',
        choices=['owner', 'admin', 'user'],
        required=True,
    )
    timezone = properties.String(
        'Name of the user\'s time zone.',
    )
    type = properties.StringChoice(
        'The type of user.',
        choices=['user', 'team'],
        required=True,
    )
