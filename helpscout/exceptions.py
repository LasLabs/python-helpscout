# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).


class HelpScoutException(Exception):
    """Base exception for HelpScout library errors."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class HelpScoutRemoteException(HelpScoutException):
    """Indicates that an error occurred when communicating with the remote."""

    def __init__(self, status_code, message):
        self.status_code = status_code
        super(HelpScoutRemoteException, self).__init__(message)

    def __str__(self):
        return '(%d) %s' % (self.status_code, self.message)


class HelpScoutValidationError(HelpScoutException):
    """Indicates an error while validating user-supplied data."""
