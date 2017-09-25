# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from datetime import datetime, date

from ..base_model import BaseModel


class Domain(properties.HasProperties):
    """This represents a full search query."""

    OR = 'OR'
    AND = 'AND'

    def __init__(self, queries=None, join_with=AND):
        """Initialize a domain, with optional queries."""
        self.query = []
        if queries is not None:
            for query in queries:
                self.add_query(query, join_with)

    @classmethod
    def from_tuple(cls, queries):
        """Create a ``Domain`` given a set of complex query tuples.

        Args:
            queries (iter): An iterator of complex queries. Each iteration
                should contain either:

                * A data-set compatible with :func:`~domain.Domain.add_query`
                * A string to switch the join type

                Example::

                    [('subject', 'Test1'),
                     'OR',
                     ('subject', 'Test2')',
                     ('subject', 'Test3')',
                     ]
                    # The above is equivalent to:
                    #    subject:'Test1' OR subject:'Test2' OR subject:'Test3'

                    [('modified_at', datetime(2017, 01, 01)),
                     ('status', 'active'),
                     ]
                    # The above is equivalent to:
                    #    modified_at:[2017-01-01T00:00:00Z TO *]
                    #    AND status:"active"

        Returns:
            Domain: A domain representing the input queries.
        """
        domain = cls()
        join_with = cls.AND
        for query in queries:
            if query in [cls.OR, cls.AND]:
                join_with = query
            else:
                domain.add_query(query, join_with)
        return domain

    def add_query(self, query, join_with=AND):
        """Join a new query to existing queries on the stack.

        Args:
            query (tuple or list or DomainCondition): The condition for the
                query. If a ``DomainCondition`` object is not provided, the
                input should conform to the interface defined in
                :func:`~.domain.DomainCondition.from_tuple`.
            join_with (str): The join string to apply, if other queries are
                already on the stack.
        """
        if not isinstance(query, DomainCondition):
            query = DomainCondition.from_tuple(query)
        if len(self.query):
            self.query.append(join_with)
        self.query.append(query)

    def __str__(self):
        """Return a string usable as the query in an API request."""
        return '(%s)' % ' '.join([str(q) for q in self.query])


class DomainCondition(properties.HasProperties):
    """This represents one condition of a domain query."""

    field = properties.String(
        'Field to search on',
        required=True,
    )
    value = properties.String(
        'String Value',
        required=True,
    )

    @property
    def field_name(self):
        """Return the name of the API field."""
        return BaseModel._to_camel_case(self.field)

    def __init__(self, field, value, **kwargs):
        """Initialize a new generic query condition.

        Args:
            field (str): Field name to search on. This should be the
                Pythonified name as in the internal models, not the
                name as provided in the API e.g. ``first_name`` for
                the Customer's first name instead of ``firstName``.
            value (mixed): The value of the field.
        """
        return super(DomainCondition, self).__init__(
            field=field, value=value, **kwargs
        )

    @classmethod
    def from_tuple(cls, query):
        """Create a condition from a query tuple.

        Args:
            query (tuple or list): Tuple or list that contains a query domain
                in the format of ``(field_name, field_value,
                field_value_to)``. ``field_value_to`` is only applicable in
                the case of a date search.

        Returns:
            DomainCondition: An instance of a domain condition. The specific
                type will depend on the data type of the first value provided
                in ``query``.
        """

        field, query = query[0], query[1:]

        try:
            cls = TYPES[type(query[0])]
        except KeyError:
            # We just fallback to the base class if unknown type.
            pass

        return cls(field, *query)

    def __str__(self):
        """Return a string usable as a query part in an API request."""
        return '%s:"%s"' % (self.field_name, self.value)


class DomainConditionBoolean(DomainCondition):
    """This represents an integer query."""

    value = properties.Bool(
        'Boolean Value',
        required=True,
    )

    def __str__(self):
        """Return a string usable as a query part in an API request."""
        value = 'true' if self.value else 'false'
        return '%s:%s' % (self.field_name, value)


class DomainConditionInteger(DomainCondition):
    """This represents an integer query."""

    value = properties.Integer(
        'Integer Value',
        required=True,
    )

    def __str__(self):
        """Return a string usable as a query part in an API request."""
        return '%s:%d' % (self.field_name, self.value)


class DomainConditionDateTime(DomainCondition):
    """This represents a date time query."""

    value = properties.DateTime(
        'Date From',
        required=True,
    )
    value_to = properties.DateTime(
        'Date To',
    )

    def __init__(self, field, value_from, value_to=None):
        """Initialize a new datetime query condition.

        Args:
            field (str): Field name to search on. This should be the
                Pythonified name as in the internal models, not the
                name as provided in the API e.g. ``first_name`` for
                the Customer's first name instead of ``firstName``.
            value_from (date or datetime): The start value of the field.
            value_to (date or datetime, optional): The ending value for
                the field. If omitted, will search to now.
        """
        return super(DomainConditionDateTime, self).__init__(
            field=field, value=value_from, value_to=value_to,
        )

    def __str__(self):
        """Return a string usable as a query part in an API request."""
        value_to = self.value_to.isoformat() if self.value_to else '*'
        return '%s:[%sZ TO %sZ]' % (
            self.field_name,
            self.value.isoformat(),
            value_to,
        )


TYPES = {
    bool: DomainConditionBoolean,
    int: DomainConditionInteger,
    date: DomainConditionDateTime,
    datetime: DomainConditionDateTime,
}


__all__ = [
    'Domain',
    'DomainCondition',
    'DomainConditionBoolean',
    'DomainConditionDateTime',
    'DomainConditionInteger',
]
