# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from requests import Session
from requests.auth import HTTPBasicAuth

from .auth_proxy import AuthProxy
from .base_api import BaseApi
from .base_model import BaseModel

from . import exceptions


class HelpScout(object):
    """This object is the primary point of interaction with HelpScout.

    Properties will be set on this ``HelpScout`` instance that will mirror
    the class names of APIs in the ``helpscout.api`` module.

    These API classes are naive of authentication, so the actual properties
    set will be using the ``AuthProxy`` class, which will transparently
    inject authentication into the API requests while still allowing for a
    naive API object.

    This allows for the ``HelpScout`` instance to act as a container for
    all of the authenticated API objects.

    Examples:

    ..code-block:: python

        from helpscout import HelpScout
        hs = HelpScout('api_key')
        for customer in hs.Customers.list():
            print(customer)

    Attributes:
        Conversations (helpscout.api.conversations.Conversations):
            Conversations API endpoint.
        Customers (helpscout.api.customers.Customers): Customers API
            endpoint.
        Mailboxes (helpscout.api.mailboxes.Mailboxes): Mailboxes API endpoint.
        Tags (helpscout.api.tags.Tags): Tags API endpoint.
        Teams (helpscout.api.teams.Teams): Teams API endpoint.
        Users (helpscout.api.users.Users): Users API endpoint.
        __apis__ (dict): References to all available APIs, keyed by class
            name.
    """

    __apis__ = {}

    def __init__(self, api_key):
        """Initialize a new HelpScout client.

        Args:
            api_key (str): The API key to use for this session.
        """
        self.session = Session()
        self.session.auth = HTTPBasicAuth(api_key, 'NoPassBecauseKey!')
        self._load_apis()

    def _load_apis(self):
        """Find available APIs and set instances property auth proxies."""
        helpscout = __import__('helpscout.apis')
        for class_name in helpscout.apis.__all__:
            if not class_name.startswith('_'):
                cls = getattr(helpscout.apis, class_name)
                api = AuthProxy(self.session, cls)
                setattr(self, class_name, api)
                self.__apis__[class_name] = api

__all__ = [
    'AuthProxy',
    'BaseApi',
    'BaseModel',
    'exceptions',
    'HelpScout',
]
