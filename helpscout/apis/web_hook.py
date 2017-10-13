# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..request_paginator import RequestPaginator
from ..models.web_hook import WebHook


class WebHook(BaseApi):
    """This represents the ``WebHook`` Endpoint.

    The following aspects are implemented:

    * `Create Web Hook
      <http://developer.helpscout.net/help-desk-api/hooks/create/>`_
      (:func:`helpscout.apis.web_hook.WebHook.create`)
    """

    __object__ = WebHook

    @classmethod
    def create(cls, session, web_hook):
        """Create a web hook.

        Note that creating a new web hook will overwrite the web hook that is
        already configured for this company. There is also no way to
        programmatically determine if a web hook already exists for the
        company. This is a limitation of the HelpScout API and cannot be
        circumvented.

        Args:
            session (requests.sessions.Session): Authenticated session.
            web_hook (helpscout.models.WebHook): The web hook to be created.

        Returns:
            bool: ``True`` if the creation was a success. Errors otherwise.
        """
        cls(
            '/hooks.json',
            data=web_hook.to_api(),
            request_type=RequestPaginator.POST,
            session=session,
        )
        return True
