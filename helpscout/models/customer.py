# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .address import Address
from .chat import Chat
from .email import Email
from .phone import Phone
from .search_customer import SearchCustomer
from .social_profile import SocialProfile
from .website import Website


class Customer(SearchCustomer):
    """This represents a customer, which is a type of person."""

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
