# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import requests

from .exceptions import HelpScoutRemoteException, HelpScoutValidationError


class RequestPaginator(object):
    """ RequestPaginator provides an iterator based upon an initial request.
    """

    # Response attributes that mean things
    PAGE_TOTAL = 'pages'  # Total number of pages
    PAGE_CURRENT = 'page'  # Current page number
    PAGE_DATA_MULTI = 'items'  # Attribute if multiple results
    PAGE_DATA_SINGLE = 'item'  # Attribute if one result

    SSL_VERIFY = True  # Verify SSL
    PAGE_SIZE = 50  # Page size returned by HelpScout

    # HTTP operation constants
    DELETE = 'delete'
    GET = 'get'
    POST = 'post'
    PUT = 'put'

    # Starting page ints
    page_current = 0
    page_total = 0

    def __init__(self, endpoint, data=None, output_type=dict,
                 request_type=GET, session=None):
        """Initialize the RequestPaginator object.

        Args:
            endpoint (str): URI endpoint to call.
            session (requests.Session): The authenticated requests session.
            data (dict): Data to be sent in the query string for the
             Request.
            output_type (type): Class type to output. Object will be
             instantiated using the current row before output.
            request_type (str): Type of request to send (``GET`` or ``POST``).
            session (requests.Session, optional): An authenticated requests
             session to use.

        Raises:
            NotImplementedError: In the event that an invalid request type was
             defined.
        """
        self.endpoint = endpoint
        self.data = data
        self.output_type = output_type
        if request_type not in (self.GET, self.POST, self.PUT, self.DELETE):
            raise NotImplementedError(
                'The `%s` request type is not implemented', request_type,
            )
        self.request_type = request_type
        self.session = session or requests.Session()

    def __iter__(self, page=1):
        """Provide an iterator for the remote request.

        The result is returned as an instantiated `self.output_type`.
        """
        self.page_current = page
        data = self.data.copy()
        result = self.call(data)
        for row in result:
            yield self.output_type(**row)
        if self.page_current < self.page_total:
            for inner_row in self.__iter__(self.page_current + 1):
                yield inner_row
        else:
            raise StopIteration()

    def call(self, data=None):
        """Generic API caller. Return the JSON decoded result.

        Args:
            data (dict, optional): Either the request parameters or the JSON
             data, depending on the request type.

        Raises:
            NotImplementedError: In the event that an invalid request type was
             defined.

        Returns:
            mixed: JSON decoded respons.
        """
        return getattr(self, self.request_type)(data)

    def delete(self, json=None):
        """Send a DELETE request and return the JSON decoded result.

        Args:
            json (dict, optional): Object to encode and send in request.

        Returns:
            mixed: JSON decoded response data.
        """
        return self._call('delete', url=self.endpoint, json=json)

    def get(self, params=None):
        """Send a POST request and return the JSON decoded result.
        
        Args:
            params (dict, optional): Mapping of parameters to send in request.
        
        Returns:
            mixed: JSON decoded response data.
        """
        return self._call('get', url=self.endpoint, params=params)

    def post(self, json=None):
        """Send a POST request and return the JSON decoded result.

        Args:
            json (dict, optional): Object to encode and send in request.

        Returns:
            mixed: JSON decoded response data.
        """
        return self._call('post', url=self.endpoint, json=json)

    def put(self, json=None):
        """Send a PUT request and return the JSON decoded result.

        Args:
            json (dict, optional): Object to encode and send in request.

        Returns:
            mixed: JSON decoded response data.
        """
        return self._call('put', url=self.endpoint, json=json)

    def _call(self, method, *args, **kwargs):
        """Call the remote service and return the response data."""

        assert self.session
        method = getattr(self.session, method)

        if not kwargs.get('verify'):
            kwargs['verify'] = self.SSL_VERIFY

        response = method(*args, **kwargs)
        response_json = response.json()

        if response.status_code < 200 or response.status_code >= 300:
            message = response_json.get('error', response_json.get('message'))
            raise HelpScoutRemoteException(response.status_code, message)

        self.page_current = response_json[self.PAGE_CURRENT]
        self.page_total = response_json[self.PAGE_TOTAL]

        try:
            return response_json[self.PAGE_DATA_MULTI]
        except KeyError:
            pass

        try:
            return [response_json[self.PAGE_DATA_SINGLE]]
        except KeyError:
            pass

        return True


