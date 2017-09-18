# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class Person(BaseModel):
    """This is a subset of the data representing a Customer, User or Team.

    The ``type`` property will specify if this person is represented by a
    ``user``, ``customer`` or ``team``.
    """

    first_name = properties.String(
        'First name',
        required=True,
    )
    last_name = properties.String(
        'Last name',
        required=True,
    )
    email = properties.String(
        'Email',
    )
    phone = properties.String(
        'Phone is only populated when the Person is a customer associated '
        'with a Conversation of type ``phone`` and a phone number was '
        'specified at the time the conversation was created.',
    )
    type = properties.StringChoice(
        'The type of person.',
        choices=['user', 'customer', 'team'],
        default='customer',
        required=True,
    )
    photo_url = properties.String(
        'The user\'s photo, if one exists.',
    )
