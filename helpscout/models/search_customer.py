# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .person import Person

from .address import Address
from .chat import Chat
from .email import Email
from .phone import Phone
from .social_profile import SocialProfile
from .website import Website


class SearchCustomer(Person):
    """This represents a customer as returned by a search."""

    full_name = properties.String(
        'Full name for the customer',
    )
    photo_type = properties.StringChoice(
        'Type of photo.',
        choices=['unknown',
                 'gravatar',
                 'twitter',
                 'facebook',
                 'googleprofile',
                 'googleplus',
                 'linkedin',
                 ],
    )
    gender = properties.StringChoice(
        'Gender of this customer.',
        choices=['female', 'male', 'unknown'],
        default='unknown',
        required=True,
    )
    age = properties.String(
        'Age (or age range) of this customer.',
    )
    organization = properties.String(
        'Company/Organization the customer identifies with.',
    )
    job_title = properties.String(
        'Job title at company/organization.',
    )
    location = properties.String(
        'Location',
    )
    emails = properties.List(
        'Email addresses for the customer.',
        prop=properties.String(''),
    )
    created_at = properties.DateTime(
        'UTC time when this customer was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this customer was modified.',
    )
