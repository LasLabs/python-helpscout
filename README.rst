|License MIT| | |Build Status| | |Test Coverage| | |Code Climate|

=========
HelpScout
=========

This library allows you to interact with HelpScout using Python.

* `Read The API Documentation <https://laslabs.github.io/python-helpscout>`_

Installation
============

Installation is easiest using Pip and PyPi::

   pip install helpscout

If you would like to contribute, or prefer Git::

   git clone https://github.com/LasLabs/python-helpscout.git
   cd python-helpscout
   pip install -r requirements.txt
   pip install .

Usage
=====

The `HelpScout object <https://laslabs.github.io/python-helpscout/helpscout.html#helpscout.HelpScout>`_
is the primary point of interaction with the HelpScout API.

Connecting to the HelpScout API will require an API Key, which is generated from
within your HelpScout account. In the below example, our key is ``API_KEY``.

.. code-block:: python

   from helpscout import HelpScout
   hs = HelpScout('API_KEY')

The HelpScout API endpoints are exposed as variables on the instantiated ``HelpScout``
object. The available endpoints are:

* `Conversations <https://laslabs.github.io/python-helpscout/helpscout.apis.html#module-helpscout.apis.conversations>`_
* `Customers <https://laslabs.github.io/python-helpscout/helpscout.apis.html#module-helpscout.apis.customers>`_
* `Mailboxes <https://laslabs.github.io/python-helpscout/helpscout.apis.html#module-helpscout.apis.mailboxes>`_
* `Tags <https://laslabs.github.io/python-helpscout/helpscout.apis.html#module-helpscout.apis.tags>`_
* `Teams <https://laslabs.github.io/python-helpscout/helpscout.apis.html#module-helpscout.apis.teams>`_
* `Users <https://laslabs.github.io/python-helpscout/helpscout.apis.html#module-helpscout.apis.users>`_

They can also be viewed from the ``__apis__`` property of ``HelpScout``::

   >>> hs.__apis__
   {'Conversations': <helpscout.auth_proxy.AuthProxy object at 0x10783ddd0>,
    'Customers': <helpscout.auth_proxy.AuthProxy object at 0x10783dd90>,
    'Mailboxes': <helpscout.auth_proxy.AuthProxy object at 0x10783ded0>,
    'Users': <helpscout.auth_proxy.AuthProxy object at 0x10783df50>,
    'Teams': <helpscout.auth_proxy.AuthProxy object at 0x10783df10>,
    }

API usage is as simple as calling the method with the required parameters:

.. code-block:: python

   for customer in hs.Customers.list():
       print(customer.first_name)

Known Issues / RoadMap
======================

* Add the ability to accept web hooks via HTTP
* Add better validations (like regexes for emails)
* Verify required attributes, particularly when creating for API instead of
  receiving
* Attachment handling in Conversations (Create/Delete Attachment)
* Raw email source handling in Conversations (Get Thread Source)
* Implement List Customers by Mailbox
* Implement Search endpoint
* Implement Workflows

Credits
=======

Contributors
------------

* Dave Lasley <dave@laslabs.com>

Maintainer
----------

.. image:: https://laslabs.com/logo.png
   :alt: LasLabs Inc.
   :target: https://laslabs.com

This module is maintained by LasLabs Inc.

.. |Build Status| image:: https://api.travis-ci.org/LasLabs/python-helpscout.svg?branch=master
   :target: https://travis-ci.org/LasLabs/python-helpscout
.. |Test Coverage| image:: https://codecov.io/gh/LasLabs/python-helpscout/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/LasLabs/python-helpscout
.. |Code Climate| image:: https://codeclimate.com/github/LasLabs/python-helpscout/badges/gpa.svg
   :target: https://codeclimate.com/github/LasLabs/python-helpscout
.. |License MIT| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT
