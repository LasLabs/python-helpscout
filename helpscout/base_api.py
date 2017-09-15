# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .request_paginator import RequestPaginator

from .base_model import BaseModel


class BaseApi(object):
    """This is the API interface object to be implemented by API adapters.
    
    It acts as a collection for the API object that it represents, passing
    through iteration to the API's request paginator.

    Attributes:
        BASE_URI (str): HelpScout API URI base.
        paginator (RequestPaginator): Object to use for producing an iterator
        representing multiple requests (API response pages). Created on init.
        __object__ (helpscout.models.BaseModel): Model object that API
        represents.
    """

    BASE_URI = 'https://api.helpscout.net/v1'

    # This should be replaced in child classes with the correct model.
    __object__ = BaseModel

    # This is set within new, after the object has been created.
    paginator = None

    def __new__(cls, endpoint, data=None,
                request_type=RequestPaginator.GET, singleton=False,
                session=None):
        """Create a new API object.
        
        Args:
            endpoint (str): The API endpoint that this represents.
            ``BASE_URI`` will be prepended, with no slashes added.
            data (dict, optional): Data to send with the request.
            request_type (str, optional): Type of request (``GET or ``POST``).
            Defaults to ``GET``.
            singleton (bool, optional): Set this to ``True`` to assert that
            there is not more than one result, and return the first result (or
            ``None`` if there is no result.
            session (requests.Session, optional): An authenticated requests
            session to use.
        
        Raises:
            HelpScoutRemoteException: If ``singleton`` is ``True``, but the
            remote API responds with more than one result.

        Returns:
            BaseApi: An instance of an API object, if ``singleton`` is
            ``False``.
            BaseModel: An instance of a Model, if ``singleton`` is
            ``True`` and there are results.
            None: If ``singleton`` is ``True`` and there are no results.
        """
        paginator = RequestPaginator(
            endpoint='%s%s' % (cls.BASE_URI, endpoint),
            data=data,
            output_type=cls.__object__.from_api,
            request_type=request_type,
            session=session,
        )
        if singleton:
            results = paginator.call(paginator.data)
            result_length = len(results)
            if result_length == 0:
                return None
            return results[0]
        obj = super(BaseApi, cls).__new__(cls)
        obj.paginator = paginator
        return obj

    def __iter__(self):
        """Pass through iteration to the API response."""
        for row in self.paginator:
            yield row
        raise StopIteration()
