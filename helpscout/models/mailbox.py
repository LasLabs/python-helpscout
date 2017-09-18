# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .folder import Folder
from .mailbox_ref import MailboxRef


class Mailbox(MailboxRef):

    slug = properties.String(
        'Key used to represent this Mailbox.',
        required=True,
    )
    email = properties.String(
        'Email address',
        required=True,
    )
    folders = properties.List(
        'Folders that this mailbox contains.',
        prop=Folder,
    )
    created_at = properties.DateTime(
        'UTC time when this mailbox was created.',
    )
    modified_at = properties.DateTime(
        'UTC time when this mailbox was modified.',
    )
