# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .web_hook import WebHook
from .web_hook_event import WebHookEvent

__all__ = [
    'WebHook',
    'WebHookEvent',
]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hmac

from base64 import b64encode
from hashlib import sha1

WEBHOOK_SECRET_KEY = 'your secret key'

def is_from_help_scout(data, signature, encoding='utf8'):
    """Validate the signature for the provided data.

        Args:
            signature (str): Signature that was provided in the
                ``X-HelpScout-Signature`` header of the request from
                HelpScout.
            data (str): Data that was provided in the request body from
                HelpScout.
            encoding (str, optional): This is the character encoding for
                the ``data`` and ``signature`` strings.

        Returns:
            bool: Whether the signature is valid for the provided data.
    """

    api_key = bytearray(WEBHOOK_SECRET_KEY, encoding)
    data = bytearray(data, encoding)
    signature = bytearray(signature, encoding)

    hash = hmac.new(api_key, data, sha1)
    encoded = b64encode(hash.digest())

    return encoded.strip() == signature.strip()

# Usage Example
signature = 'I1KlvGppYqvFTJgJ9jezdQMDiyI='
data = '{"ticket":{"id":"1","number":"2"},"customer":{"id":"1","fname":"Jackie","lname":"Chan","email":"jackie.chan@somewhere.com","emails":["jackie.chan@somewhere.com"]}}'

print('Request validation response was',
      is_from_help_scout(data, signature))
