# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.tag import Tag


class Tags(BaseApi):
    """This represents the ``Tags`` Endpoint.

    The following aspects are implemented:
    * `List Tags
      <http://developer.helpscout.net/help-desk-api/tags/list/>`_
    """

    __object__ = Tag

    @classmethod
    def list(cls, session):
        """List the tags.

        Args:
            session (requests.Session): Authenticated requests Session.

        Returns:
            RequestPaginator of Tag: Tags iterator.
        """
        return cls('/tags.json', session=session)
