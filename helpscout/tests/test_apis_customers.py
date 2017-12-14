# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .api_common import ApiCommon, recorder


class TestApisCustomers(ApiCommon):
    """Tests the Customers API endpoint."""

    def setUp(self):
        super(TestApisCustomers, self).setUp()
        self.__endpoint__ = self.api.Customers

    @recorder.use_cassette()
    def test_apis_customers_create(self):
        """It should create and return a Customer."""
        self._test_create(self._get_customer(strip_id=True))

    @recorder.use_cassette()
    def test_apis_customers_get(self):
        """It should return the customer."""
        self._test_get(self._get_customer())

    @recorder.use_cassette()
    def test_apis_customers_delete(self):
        """It should not be implemented."""
        with self.assertRaises(NotImplementedError):
            self.__endpoint__.delete(self._get_customer())

    @recorder.use_cassette()
    def test_apis_customers_list(self):
        """It should list the customers in the mailbox."""
        self._test_list()

    @recorder.use_cassette()
    def test_apis_customers_search(self):
        """It should search for and return the customer."""
        self._test_search(self._get_customer())

    @recorder.use_cassette()
    def test_apis_customers_update(self):
        """It should update the customer."""
        self._test_update(
            self._get_customer(strip_id=True),
            'first_name',
            'A new name',
        )
