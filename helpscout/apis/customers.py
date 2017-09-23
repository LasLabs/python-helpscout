# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .. import BaseApi

from ..models.customer import Customer
from ..models.search_customer import SearchCustomer

from ..request_paginator import RequestPaginator


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

    @classmethod
    def create(cls, session, customer, _reload=False):
        """Create a customer.

        Args:
            session (requests.Session): Authenticated requests Session.
            customer (Customer): The customer to be created.
            _reload (bool, optional): Set this request parameter to ``True``
            to return the created conversation in the response.

        Returns:
            bool: Success status, if ``_reload`` is ``False``.
            Customer: Newly created customer, if ``_reload`` is ``True``.
        """
        data = {
            'customer': customer.to_api(),
            'reload': _reload,
        }
        return cls(
            '/customers.json',
            data=data,
            request_type=RequestPaginator.POST,
            singleton=True,
            session=session,
        )

    @classmethod
    def get(cls, session, customer_id):
        """Return a specific customer.

        Args:
            session (requests.Session): Authenticated requests Session.
            customer_id (int): The ID of the customer to get.

        Returns:
            Customer: A customer singleton, if existing.
            None: If no match for the ID.
        """
        return cls(
            '/customers/%d.json' % customer_id,
            singleton=True,
            session=session,
        )

    @classmethod
    def list(cls, session, first_name=None, last_name=None, email=None,
             modified_since=None):
        """List the customers.

        Customers can be filtered on any combination of first name, last name,
        email, and modifiedSince.

        Args:
            session (requests.Session): Authenticated requests Session.
            first_name (str, optional): First name of customer.
            last_name (str, optional): Last name of customer.
            email (str, optional): Email address of customer.
            modified_since (datetime, optional): If modified after this date.

        Returns:
            RequestPaginator of Customer: Customers iterator.
        """
        data = cls.__object__.get_non_empty_vals({
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'modifiedSince': modified_since,
        })
        return cls('/customers.json', data, session=session)

    @classmethod
    def search(cls, session, queries):
        """Search for a customer given a domain.

        Args:
            session (requests.Session): Authenticated requests Session.
            queries (Domain | iter): The queries for the domain. If a
                ``Domain`` object is provided, it will simply be returned.
                Otherwise, a ``Domain`` object will be generated from the
                complex queries. In this case, the queries should conform
                to the interface in
                :func:`helpscout.domain.Domain.from_tuple`.

        Returns:
            RequestPaginator of SearchCustomer: SearchCustomer iterator.
        """
        domain = cls.get_search_domain(queries)
        return cls(
            '/search/conversations.json',
            data={'query': str(domain)},
            session=session,
            out_type=SearchCustomer,
        )

    @classmethod
    def update(cls, session, customer, _reload=False):
        """Update a customer.

        Args:
            session (requests.Session): Authenticated requests Session.
            customer (Customer): The customer to be updated.
            _reload (bool, optional): Set this request parameter to ``True``
            to return the created conversation in the response.

        Returns:
            bool: Success status, if ``_reload`` is ``False``.
            Customer: Freshly updated customer, if ``_reload`` is ``True``.
        """
        data = {
            'customer': customer,
            'reload': _reload,
        }
        return cls(
            '/customers/%d.json' % customer.id,
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
        )
