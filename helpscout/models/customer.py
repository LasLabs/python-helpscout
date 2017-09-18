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


class Customer(Person):
    """This represents a customer, which is a type of person."""

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
    background = properties.String(
        'This is the Notes field from the user interface.',
    )
    address = properties.Instance(
        'The address for this customer.',
        instance_class=Address,
    )
    social_profiles = properties.List(
        'Social profiles that represent this customer.',
        prop=SocialProfile,
    )
    emails = properties.List(
        'Email addresses for this customer.',
        prop=Email,
    )
    phones = properties.List(
        'Phone numbers for this customer.',
        prop=Phone,
    )
    chats = properties.List(
        'Chat addresses for this customer.',
        prop=Chat,
    )
    websites = properties.List(
        'Websites for this customer.',
        prop=Website,
    )
    created_at = properties.DateTime(
        'UTC time when this customer was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this customer was modified.',
    )
