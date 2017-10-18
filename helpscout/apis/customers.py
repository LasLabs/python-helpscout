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
    def create(cls, session, customer):
        """Create a customer.

        Args:
            session (requests.sessions.Session): Authenticated session.
            customer (helpscout.models.Customer): The customer to be created.

        Returns:
            helpscout.models.Customer: Newly created customer.
        """
        data = {
            'customer': customer.to_api(),
            'reload': True,
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
            session (requests.sessions.Session): Authenticated session.
            customer_id (int): The ID of the customer to get.

        Returns:
            helpscout.models.Customer: A customer singleton, if existing.
                Otherwise ``None``.
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
        domain = cls.get_search_domain(queries)
        return cls(
            '/search/customers.json',
            data={'query': str(domain)},
            session=session,
            out_type=SearchCustomer,
        )

    @classmethod
    def update(cls, session, customer):
        """Update a customer.

        Args:
            session (requests.sessions.Session): Authenticated session.
            customer (helpscout.models.Customer): The customer to be updated.

        Returns:
            helpscout.models.Customer: Freshly updated customer.
        """
        data = customer.to_api()
        data['reload'] = True
        return cls(
            '/customers/%d.json' % customer.id,
            data=data,
            request_type=RequestPaginator.PUT,
            singleton=True,
            session=session,
        )
