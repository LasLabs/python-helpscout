# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import base64
import properties

from .. import BaseModel


class AttachmentData(BaseModel):

    data = properties.String(
        'base64 encoded data.',
    )

    @property
    def raw_data(self):
        """Raw (decoded) attachment data (possibly binary)."""
        return self.data and base64.b64decode(self.data)

    @raw_data.setter
    def raw_data(self, value):
        """Set the base64 encoded data using a raw value or file object."""
        if value:
            try:
                value = value.read()
            except AttributeError:
                pass
            b64 = base64.b64encode(value.encode('utf-8'))
            self.data = b64.decode('utf-8')

    @raw_data.deleter
    def raw_data(self):
        self.data = None
