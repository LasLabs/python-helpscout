# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties
import re

from .exceptions import HelpScoutValidationError


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
            HelpScoutValidationError: In the event that an unexpected property
            is received.

        Returns:
            BaseModel: Instantiated model using the API values.
        """

        vals = cls.get_non_empty_vals({
            cls._to_snake_case(k): v for k, v in kwargs.items()
        })

        for attribute, value in vals.items():

            prop = cls._props.get(attribute)

            if not prop:
                raise HelpScoutValidationError(
                    '"%s" is not a valid property for "%s".' % (
                        attribute, cls,
                    ),
                )

            if isinstance(prop, properties.Instance):
                vals[attribute] = prop.instance_class.from_api(**value)

            elif isinstance(prop, properties.List):
                vals[attribute] = [
                    prop.prop.instance_class.from_api(**v) for v in value
                ]

        return cls(**vals)

    def to_api(self):
        """Return a dictionary to send to the API.
        
        Returns:
            dict: Mapping representing this object that can be sent to the
            API.
        """
        vals = {}
        for attribute, attribute_type in self._props.items():

            prop = getattr(self, attribute)

            if isinstance(attribute_type, properties.Instance):
                    prop = prop.to_api()

            elif isinstance(attribute_type, properties.List):
                prop = [p.to_api() for p in prop]

            vals[self._to_camel_case(attribute)] = prop

        return vals

    @staticmethod
    def get_non_empty_vals(mapping):
        """Return the mapping without any ``None`` values."""
        return {
            k: v for k, v in mapping.items() if v is not None
        }

    @staticmethod
    def _to_snake_case(string):
        sub_string = r'\1_\2'
        string = REGEX_CAMEL_FIRST.sub(sub_string, string)
        return REGEX_CAMEL_SECOND.sub(sub_string, string).lower()

    @staticmethod
    def _to_camel_case(string):
        components = string.split('_')
        return '%s%s' % (
            components[0],
            ''.join(c.title() for c in components[1:]),
        )
