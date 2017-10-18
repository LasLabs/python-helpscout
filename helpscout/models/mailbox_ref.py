# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .. import BaseModel


class MailboxRef(BaseModel):
    """The mailbox ref is a subset of the full Mailbox object."""

    name = properties.String(
        'Name of the Mailbox.',
        required=True,
    )
