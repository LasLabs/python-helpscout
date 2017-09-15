# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties
import unittest

try:
    import mock
except ImportError:
    mock = unittest.mock

from .. import BaseModel
from ..exceptions import HelpScoutValidationError


class TestModel(BaseModel):
    a_key = properties.String('A key')
    sub_instance = properties.Instance(
        'Sub Instance', instance_class=BaseModel,
    )
    list = properties.List(
        'List', prop=properties.Instance('List Instance',
                                         instance_class=BaseModel),
    )


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        super(TestBaseModel, self).setUp()
        self.test_values = {
            'aKey': 'value',
            'subInstance': {
                'id': 1234,
            },
            'list': [
                {'id': 4321},
            ],
        }
        self.internal_values = {
            'a_key': self.test_values['aKey'],
            'sub_instance': self.test_values['subInstance'],
            'list': self.test_values['list'],
        }

    def new_record(self):
        return TestModel.from_api(**self.test_values)

    def test_from_api_new_instance(self):
        """It should return a new instance of the class."""
        self.assertIsInstance(self.new_record(), TestModel)

    def test_from_api_camel_to_snake(self):
        """It should call the init with snake cased keys."""
        self.assertEqual(self.new_record().a_key, self.test_values['aKey'])

    def test_from_api_invalid_attribute(self):
        """It should not allow invalid attribute assignments."""
        with self.assertRaises(HelpScoutValidationError):
            BaseModel.from_api(**{'no exist': 'value'})

    def test_from_api_sub_instance(self):
        """It should properly instantiate sub-instances."""
        self.assertIsInstance(self.new_record().sub_instance, BaseModel)

    def test_from_api_list(self):
        """It should properly convert lists of instances."""
        res = self.new_record()
        self.assertIsInstance(res.list, list)
        self.assertIsInstance(res.list[0], BaseModel)

    def test_to_api_camel_case(self):
        """It should properly camel case the API args."""
        res = self.new_record().to_api()
        self.assertEqual(res['aKey'], self.internal_values['a_key'])

    def test_to_api_instance(self):
        """It should properly convert sub-instances to dict."""
        res = self.new_record().to_api()
        self.assertIsInstance(res['subInstance'], dict)

    def test_to_api_list(self):
        """It should properly convert sub-instances within lists props."""
        res = self.new_record().to_api()
        self.assertIsInstance(res['list'], list)
        self.assertIsInstance(res['list'][0], dict)

    def test_get_non_empty_vals(self):
        """It should return the dict without NoneTypes."""
        expect = {
            'good_int': 1234,
            'good_false': False,
            'good_true': True,
            'bad': None,
        }
        res = BaseModel.get_non_empty_vals(expect)
        del expect['bad']
        self.assertDictEqual(res, expect)
