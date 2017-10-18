# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .base_model import BaseModel
from .domain import Domain
from .request_paginator import RequestPaginator


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
                session=None, out_type=None):
        """Create a new API object.

        Args:
            endpoint (str): The API endpoint that this represents.
                ``BASE_URI`` will be prepended, with no slashes added.
            data (dict, optional): Data to send with the request.
            request_type (str, optional): Type of request (``GET or ``POST``).
                Defaults to ``GET``.
            singleton (bool, optional): Set this to ``True`` to assert that
                there is not more than one result, and return the first result
                (or ``None`` if there is no result).
            session (requests.Session, optional): An authenticated requests
                session to use.
            out_type (BaseModel, optional): If set, this object will be used
                for the creation of the models, instead of the one set in
                ``cls.__object__``.

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
        if out_type is None:
            out_type = cls.__object__
        paginator = RequestPaginator(
            endpoint='%s%s' % (cls.BASE_URI, endpoint),
            data=data,
            output_type=out_type.from_api,
            request_type=request_type,
            session=session,
        )
        if singleton:
            results = paginator.call(paginator.data)
            result_length = len(results)
            if result_length == 0:
                return None
            return out_type.from_api(**results[0])
        obj = super(BaseApi, cls).__new__(cls)
        obj.paginator = paginator
        return obj

    def __iter__(self):
        """Pass through iteration to the API response."""
        for row in self.paginator:
            yield row
        raise StopIteration()

    @classmethod
    def new_object(cls, data):
        """Return a new object of the correct type from the data.

        Args:
            data (dict): Data dictionary that should be converted to an
                object. It can use either camelCase keys or snake_case.

        Returns:
            BaseModel: A model of the type declared in ``cls.__object__``.
        """
        return cls.__object__.from_api(**data)

    @staticmethod
    def get_search_domain(queries):
        """Helper method to create search domains if needed.

        Args:
            queries (Domain or iter): The queries for the domain. If a
                ``Domain`` object is provided, it will simply be returned.
                Otherwise, a ``Domain`` object will be generated from the
                complex queries. In this case, the queries should conform
                to the interface in
                :func:`helpscout.domain.Domain.from_tuple`.

        Returns:
            Domain: Either the provided domain, or one created from
                ``queries``.
        """
        if isinstance(queries, Domain):
            return queries
        return Domain.from_tuple(queries)
