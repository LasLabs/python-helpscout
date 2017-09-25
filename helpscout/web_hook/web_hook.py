# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import hmac
import json
import properties

from base64 import b64encode
from hashlib import sha1
from six import string_types

from .web_hook_event import WebHookEvent

from ..exceptions import HelpScoutSecurityException


class HelpScoutWebHook(properties.HasProperties):
    """This provides the ability to easily process web hook events."""

    secret_key = properties.String(
        'Secret key that should be used to validate requests against. This '
        'is configured while setting up the web hook in your HelpScout '
        'account.',
        required=True,
    )

    def receive(self, event_type, signature, data_str):
        """Receive a web hook for the event and signature.

        Args:
            event_type (str): Name of the event that was received (from the
                request ``X-HelpScout-Event`` header).
            signature (str): The signature that was received, which serves as
                authentication (from the request ``X-HelpScout-Signature``
                header).
            data_str (str): The raw data that was posted by HelpScout
                to the web hook. This must be the raw string, because if it
                is parsed with JSON it will lose its ordering and not pass
                signature validation.

        Raises:
            helpscout.exceptions.HelpScoutSecurityException: If an invalid
                signature is provided, and ``raise_if_invalid`` is ``True``.

        Returns:
            helpscout.web_hook.WebHookEvent: The authenticated web hook
                request.
        """

        if not self.validate_signature(signature, data_str):
            raise HelpScoutSecurityException(
                'The signature provided by this request was invalid.',
            )

        return WebHookEvent(
            event_type=event_type,
            record=json.loads(data_str),
        )

    def validate_signature(self, signature, data, encoding='utf8'):
        """Validate the signature for the provided data.

        Args:
            signature (str or bytes or bytearray): Signature that was provided
                for the request.
            data (str or bytes or bytearray): Data string to validate against
                the signature.
            encoding (str, optional): If a string was provided for ``data`` or
                ``signature``, this is the character encoding.

        Returns:
            bool: Whether the signature is valid for the provided data.
        """

        if isinstance(data, string_types):
            data = bytearray(data, encoding)
        if isinstance(signature, string_types):
            signature = bytearray(signature, encoding)

        secret_key = bytearray(self.secret_key, 'utf8')
        hashed = hmac.new(secret_key, data, sha1)
        encoded = b64encode(hashed.digest())

        return encoded.strip() == signature.strip()
