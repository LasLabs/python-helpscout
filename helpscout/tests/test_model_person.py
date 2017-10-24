# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..models.person import Person


class TestPerson(unittest.TestCase):

    def new_record(self, type):
        test_values = {
            'firstName': 'Boo',
            'lastName': 'Radley',
            'type': type,
        }
        return Person.from_api(**test_values)

    def setter_tester(self, customer_person_type, expected):
        person = self.new_record('customer')
        person.customer_person_type = customer_person_type
        self.assertEqual(person.type, expected)

    def test_customer_person_type_customer(self):
        """It should properly set customer_person_type to True when person
        type is 'customer'"""
        self.assertTrue(self.new_record('customer').customer_person_type)

    def test_customer_person_type_user(self):
        """It should properly set customer_person_type to False when person
        type is not 'customer'"""
        self.assertFalse(self.new_record('user').customer_person_type)

    def test_customer_person_type_setter_true(self):
        """It should properly set type to 'customer' when customer_person_type
        is set as True"""
        self.setter_tester(True, 'customer')

    def test_customer_person_type_setter_false(self):
        """It should properly set type to 'user' when customer_person_type
        is set as False"""
        self.setter_tester(False, 'user')
