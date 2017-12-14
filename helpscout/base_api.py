# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .base_model import BaseModel
from .domain import Domain
from .exceptions import HelpScoutRemoteException
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

    # This should be replaced with the endpoint, such as ``customers``
    __endpoint__ = None

    # Override this to disallow certain CRUD operations
    __implements__ = ['create', 'get', 'update', 'delete', 'search', 'list']

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
            try:
                result = results[0]
            except (IndexError, TypeError):
                return None
            return out_type.from_api(**result)
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

    @classmethod
    def create(cls, session, record, endpoint_override=None, out_type=None,
               **add_params):
        """Create an object on HelpScout.

        Args:
            session (requests.sessions.Session): Authenticated session.
            record (helpscout.BaseModel): The record to be created.
            endpoint_override (str, optional): Override the default
                endpoint using this.
            out_type (helpscout.BaseModel, optional): The type of record to
                output. This should be provided by child classes, by calling
                super.
            **add_params (mixed): Add these to the request parameters.

        Returns:
            helpscout.models.BaseModel: Newly created record. Will be of the
        """
        cls._check_implements('create')
        data = record.to_api()
        params = {
            'reload': True,
        }
        params.update(**add_params)
        data.update(params)
        return cls(
            endpoint_override or '/%s.json' % cls.__endpoint__,
            data=data,
            request_type=RequestPaginator.POST,
            singleton=True,
            session=session,
            out_type=out_type,
        )

    @classmethod
    def delete(cls, session, record, endpoint_override=None, out_type=None):
        """Delete a record.

        Args:
            session (requests.sessions.Session): Authenticated session.
            record (helpscout.BaseModel): The record to be deleted.
            endpoint_override (str, optional): Override the default
                endpoint using this.
            out_type (helpscout.BaseModel, optional): The type of record to
                output. This should be provided by child classes, by calling
                super.

        Returns:
            NoneType: Nothing.
        """
        cls._check_implements('delete')
        return cls(
            endpoint_override or '/%s/%s.json' % (
                cls.__endpoint__, record.id,
            ),
            request_type=RequestPaginator.DELETE,
            singleton=True,
            session=session,
            out_type=out_type,
        )

    @classmethod
    def get(cls, session, record_id, endpoint_override=None):
        """Return a specific record.

        Args:
            session (requests.sessions.Session): Authenticated session.
            record_id (int): The ID of the record to get.
            endpoint_override (str, optional): Override the default
                endpoint using this.

        Returns:
            helpscout.BaseModel: A record singleton, if existing. Otherwise
                ``None``.
        """
        cls._check_implements('get')
        try:
            return cls(
                endpoint_override or '/%s/%d.json' % (
                    cls.__endpoint__, record_id,
                ),
                singleton=True,
                session=session,
            )
        except HelpScoutRemoteException as e:
            if e.status_code == 404:
                return None
            else:
                raise

    @classmethod
    def list(cls, session, endpoint_override=None, data=None):
        """Return records in a mailbox.

        Args:
            session (requests.sessions.Session): Authenticated session.
            endpoint_override (str, optional): Override the default
                endpoint using this.
            data (dict, optional): Data to provide as request parameters.

        Returns:
            RequestPaginator(output_type=helpscout.BaseModel): Results
                iterator.
        """
        cls._check_implements('list')
        return cls(
            endpoint_override or '/%s.json' % cls.__endpoint__,
            data=data,
            session=session,
        )

    @classmethod
    def search(cls, session, queries, out_type):
        """Search for a record given a domain.

        Args:
            session (requests.sessions.Session): Authenticated session.
            queries (helpscout.models.Domain or iter): The queries for the
                domain. If a ``Domain`` object is provided, it will simply be
                returned. Otherwise, a ``Domain`` object will be generated
                from the complex queries. In this case, the queries should
                conform to the interface in
                :func:`helpscout.domain.Domain.from_tuple`.
            out_type (helpscout.BaseModel): The type of record to output. This
                should be provided by child classes, by calling super.

        Returns:
            RequestPaginator(output_type=helpscout.BaseModel): Results
                iterator of the ``out_type`` that is defined.
        """
        cls._check_implements('search')
        domain = cls.get_search_domain(queries)
        return cls(
            '/search/%s.json' % cls.__endpoint__,
            data={'query': str(domain)},
            session=session,
            out_type=out_type,
        )

    @classmethod
    def update(cls, session, record):
        """Update a record.

        Args:
            session (requests.sessions.Session): Authenticated session.
            record (helpscout.BaseModel): The record to
                be updated.

        Returns:
            helpscout.BaseModel: Freshly updated record.
        """
        cls._check_implements('update')
        data = record.to_api()
        del data['id']
        data['reload'] = True
        return cls(
            '/%s/%s.json' % (cls.__endpoint__, record.id),
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
        )

    @classmethod
    def _check_implements(cls, check_type):
        if check_type not in cls.__implements__:
            raise NotImplementedError
