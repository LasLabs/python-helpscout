# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.customer import Customer
from ..models.search_customer import SearchCustomer


class Customers(BaseApi):
    """This represents the ``Customers`` Endpoint.

    The following aspects are implemented:

    * `List Customers
      <http://developer.helpscout.net/help-desk-api/customers/list/>`_
      (:func:`helpscout.apis.customers.Customers.list`)
    * `Search Customers
      <http://developer.helpscout.net/help-desk-api/search/customers/>`_
      (:func:`helpscout.apis.customers.Customers.search`)
    * `Get Customer
      <http://developer.helpscout.net/help-desk-api/customers/get/>`_
      (:func:`helpscout.apis.customers.Customers.get`)
    * `Create Customer
      <http://developer.helpscout.net/help-desk-api/customers/create/>`_
      (:func:`helpscout.apis.customers.Customers.create`)
    * `Update Customer
      <http://developer.helpscout.net/help-desk-api/customers/update/>`_
      (:func:`helpscout.apis.customers.Customers.update`)
    """

    __object__ = Customer
    __endpoint__ = 'customers'
    __implements__ = ['create', 'get', 'update', 'search', 'list']

    @classmethod
    def list(cls, session, first_name=None, last_name=None, email=None,
             modified_since=None):
        """List the customers.

        Customers can be filtered on any combination of first name, last name,
        email, and modifiedSince.

        Args:
            session (requests.sessions.Session): Authenticated session.
            first_name (str, optional): First name of customer.
            last_name (str, optional): Last name of customer.
            email (str, optional): Email address of customer.
            modified_since (datetime.datetime, optional): If modified after
                this date.

        Returns:
            RequestPaginator(output_type=helpscout.models.Customer): Customers
                iterator.
        """
        return super(Customers, cls).list(
            session,
            data=cls.__object__.get_non_empty_vals({
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'modifiedSince': modified_since,
            })
        )

    @classmethod
    def search(cls, session, queries):
        """Search for a customer given a domain.

        Args:
            session (requests.sessions.Session): Authenticated session.
            queries (helpscout.models.Domain or iter): The queries for the
                domain. If a ``Domain`` object is provided, it will simply be
                returned. Otherwise, a ``Domain`` object will be generated
                from the complex queries. In this case, the queries should
                conform to the interface in
                :func:`helpscout.domain.Domain.from_tuple`.

        Returns:
            RequestPaginator(output_type=helpscout.models.SearchCustomer):
                SearchCustomer iterator.
        """
        return super(Customers, cls).search(session, queries, SearchCustomer)
