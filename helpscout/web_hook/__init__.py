# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

__all__ = [
    'HelpScoutWebHook',
    'WebHookEvent',
]


import hmac
import json
import properties

from base64 import b64encode
from hashlib import sha1
from six import string_types

from ..models import Conversation, Customer, Rating, WebHook, WebHookEvent

from ..exceptions import HelpScoutSecurityException


class HelpScoutWebHook(WebHook):
    """This provides the ability to easily create & process web hook events.
    """

    helpscout = properties.Instance(
        'The authenticated HelpScout object. Used for create.',
        # This cannot be defined as a HelpScout object due to circular depends
        instance_class=object,
    )

    def create(self):
        """Create the web hook on HelpScout."""
        assert self.helpscout
        return self.helpscout.WebHook.create(self)

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

        return HelpScoutWebHookEvent(
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


class HelpScoutWebHookEvent(WebHookEvent):
    """This represents an authenticated web hook request.

    Note that this object is meant to represent an authenticated Web Hook,
    and therefore is completely naive of all things authentication. Any
    request authentication/validation should happen in the ``WebHook``.
    """

    # Map the event prefixes to their corresponding data models.
    EVENT_PREFIX_TO_MODEL = {
        'convo': Conversation,
        'customer': Customer,
        'satisfaction': Rating,
    }

    def __init__(self, *args, **kwargs):
        """Parse raw record data if required.

        Args:
            record (dict or BaseModel): The record data that was received for
                the request. If it is a ``dict``, the data will be parsed
                using the proper model's ``from_api`` method.
        """
        if isinstance(kwargs.get('record'), dict):
            prefix, _ = kwargs['event_type'].split('.', 1)
            model = self.EVENT_PREFIX_TO_MODEL[prefix]
            kwargs['record'] = model.from_api(**kwargs['record'])
        super(WebHookEvent, self).__init__(*args, **kwargs)
