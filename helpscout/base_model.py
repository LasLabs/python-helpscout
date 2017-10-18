# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties
import re

from .exceptions import HelpScoutValidationException


# Identify lowerCamelCase strings.
# https://stackoverflow.com/a/1176023/861399
REGEX_CAMEL_FIRST = re.compile(r'(.)([A-Z][a-z]+)')
REGEX_CAMEL_SECOND = re.compile(r'([a-z0-9])([A-Z])')


class BaseModel(properties.HasProperties):
    """This is the model that all other models inherit from.

    It provides some convenience functions, and the standard ``id`` property.
    """

    id = properties.Integer(
        'Unique identifier',
    )

    @classmethod
    def from_api(cls, **kwargs):
        """Create a new instance from API arguments.

        This will switch camelCase keys into snake_case for instantiation.

        It will also identify any ``Instance`` or ``List`` properties, and
        instantiate the proper objects using the values. The end result being
        a fully Objectified and Pythonified API response.

        Raises:
            HelpScoutValidationException: In the event that an unexpected
             property is received.

        Returns:
            BaseModel: Instantiated model using the API values.
        """

        vals = cls.get_non_empty_vals({
            cls._to_snake_case(k): v for k, v in kwargs.items()
        })
        vals.update({
            attr: cls._parse_property(attr, val) for attr, val in vals.items()
        })
        return cls(**vals)

    def get(self, key, default=None):
        """Return the field indicated by the key, if present."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def to_api(self):
        """Return a dictionary to send to the API.

        Returns:
            dict: Mapping representing this object that can be sent to the
             API.
        """
        vals = {}
        for attribute, attribute_type in self._props.items():
            prop = getattr(self, attribute)
            vals[self._to_camel_case(attribute)] = self._to_api_value(
                attribute_type, prop,
            )
        return vals

    def _to_api_value(self, attribute_type, value):
        """Return a parsed value for the API."""

        if not value:
            return None

        if isinstance(attribute_type, properties.Instance):
            return value.to_api()

        if isinstance(attribute_type, properties.List):
            return self._parse_api_value_list(value)

        return attribute_type.serialize(value)

    def _parse_api_value_list(self, values):
        """Return a list field compatible with the API."""
        try:
            return [v.to_api() for v in values]
        # Not models
        except AttributeError:
            return list(values)

    @staticmethod
    def get_non_empty_vals(mapping):
        """Return the mapping without any ``None`` values."""
        return {
            k: v for k, v in mapping.items() if v is not None
        }

    @classmethod
    def _parse_property(cls, name, value):
        """Parse a property received from the API into an internal object.

        Args:
            name (str): Name of the property on the object.
            value (mixed): The unparsed API value.

        Returns:
            mixed: A value compatible with the internal models.
        """

        prop = cls._props.get(name)

        if not prop:
            raise HelpScoutValidationException(
                '"%s" is not a valid property for "%s".' % (
                    name, cls,
                ),
            )

        if isinstance(prop, properties.Instance):
            return prop.instance_class.from_api(**value)

        elif isinstance(prop, properties.List):
            return cls._parse_property_list(prop, value)

        return value

    @staticmethod
    def _parse_property_list(prop, value):
        """Parse a list property and return a list of the results."""
        attributes = []
        for v in value:
            try:
                attributes.append(
                    prop.prop.instance_class.from_api(**v),
                )
            except AttributeError:
                attributes.append(v)
        return attributes

    @staticmethod
    def _to_snake_case(string):
        """Return a snake cased version of the input string.

        Args:
            string (str): A camel cased string.

        Returns:
            str: A snake cased string.
        """
        sub_string = r'\1_\2'
        string = REGEX_CAMEL_FIRST.sub(sub_string, string)
        return REGEX_CAMEL_SECOND.sub(sub_string, string).lower()

    @staticmethod
    def _to_camel_case(string):
        """Return a camel cased version of the input string.

        Args:
            string (str): A snake cased string.

        Returns:
            str: A camel cased string.
        """
        components = string.split('_')
        return '%s%s' % (
            components[0],
            ''.join(c.title() for c in components[1:]),
        )

    def __getitem__(self, item):
        """Return the field indicated by the key, if present.

        This is better than using ``getattr`` because it will not expose any
        properties that are not meant to be fields for the object.

        Raises:
            KeyError: In the event that the field doesn't exist.
        """
        self.__check_field(item)
        return getattr(self, item)

    def __setitem__(self, key, value):
        """Return the field indicated by the key, if present.

        This is better than using ``getattr`` because it will not expose any
        properties that are not meant to be fields for the object.

        Raises:
            KeyError: In the event that the field doesn't exist.
        """
        self.__check_field(key)
        return setattr(self, key, value)

    def __check_field(self, key):
        """Raises a KeyError if the field doesn't exist."""
        if not self._props.get(key):
            raise KeyError(
                'The field "%s" does not exist on "%s"' % (
                    key, self.__class__.__name__,
                ),
            )
