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
      (:func:`helpscout.apis.tags.Tags.list`)
    """

    __object__ = Tag
    __endpoint__ = 'tags'
    __implements__ = ['list']
