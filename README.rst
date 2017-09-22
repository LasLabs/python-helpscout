|License MIT| | |PyPi Package| | |PyPi Versions|

|Build Status| | |Test Coverage| | |Code Climate|

=========
HelpScout
=========

This library allows you to interact with HelpScout using Python.

* `Read The API Documentation <https://laslabs.github.io/python-helpscout>`_

.. contents:: Table of Contents

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

Connection
----------

Connecting to the HelpScout API will require an API Key, which is generated from
within your HelpScout account. In the below example, our key is ``API_KEY``.

.. code-block:: python

   from helpscout import HelpScout
   hs = HelpScout('API_KEY')

API Endpoints
-------------

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

API usage is as simple as calling the method with the required parameters and
iterating the results:

.. code-block:: python

   for customer in hs.Customers.list(first_name='Help', last_name='Scout'):
       print(customer)
       print(customer.serialize())

The output from the above would look something like the below when using the
HelpScout demo data:

.. code-block:: python

   # This is the customer object itself (first print)
   <helpscout.models.customer.Customer object at 0x10783df10>
   # This is the serialized form of the customer (second print)
   {'chats': [],
    'social_profiles': [],
    'first_name': u'Help',
    'last_name': u'Scout',
    'phones': [],
    'created_at': '2017-09-16T18:38:37Z',
    'modified_at': '2017-09-16T18:38:37Z',
    u'__class__': 'Customer',
    'websites': [],
    'id': 143161083,
    'location': u'Boston, MA',
    'full_name': u'Help Scout',
    'gender': 'unknown',
    'photo_type': 'gravatar',
    'type': 'customer',
    'emails': [],
    'photo_url': u'https://secure.gravatar.com/avatar/7d599977ec288a9141317b352c04d497'}

In some instances, such as in the case of browsing for a record by its ID, a
singleton is expected. In these instances, the singleton is directly used
instead of iterated

.. code-block:: python

   >>> customer = hs.Customers.get(143161083)
   >>> customer
   <helpscout.models.customer.Customer object at 0x101723e50>
   >>> from pprint import pprint
   >>> pprint(customer.serialize())
   {u'__class__': 'Customer',
    'address': {u'__class__': 'Address',
                'city': u'Boston',
                'country': u'US',
                'created_at': '2017-09-16T18:38:37Z',
                'id': 4996350,
                'lines': [u'131 Tremont Street', u'3rd Floor'],
                'postal_code': u'02111-1338',
                'state': u'MA'},
    'chats': [],
    'created_at': '2017-09-16T18:38:37Z',
    'emails': [{u'__class__': 'Email',
                'id': 189240662,
                'location': 'work',
                'value': u'help@helpscout.net'}],
    'first_name': u'Help',
    'full_name': u'Help Scout',
    'gender': 'unknown',
    'id': 143161083,
    'last_name': u'Scout',
    'location': u'Boston, MA',
    'modified_at': '2017-09-16T18:38:37Z',
    'phones': [{u'__class__': 'Phone',
                'id': 189240668,
                'location': 'work',
                'value': u'855-435-7726'}],
    'photo_type': 'gravatar',
    'photo_url': u'https://secure.gravatar.com/avatar/7d599977ec288a9141317b352c04d497',
    'social_profiles': [{u'__class__': 'SocialProfile',
                         'id': 189240667,
                         'type': 'twitter',
                         'value': u'http://twitter.com/helpscout'},
                        {u'__class__': 'SocialProfile',
                         'id': 189240663,
                         'type': 'twitter',
                         'value': u'https://twitter.com/helpscout'},
                        {u'__class__': 'SocialProfile',
                         'id': 189240664,
                         'type': 'twitter',
                         'value': u'https://twitter.com/HelpScoutDev'}],
    'type': 'customer',
    'websites': [{u'__class__': 'Website',
                  'id': 189240670,
                  'value': u'http://developer.helpscout.net'},
                 {u'__class__': 'Website',
                  'id': 189240665,
                  'value': u'http://status.helpscout.net/'},
                 {u'__class__': 'Website',
                  'id': 189240666,
                  'value': u'http://www.helpscout.com'},
                 {u'__class__': 'Website',
                  'id': 189240671,
                  'value': u'http://www.helpscout.net'}]}

Note that all of the API responses will be parsed, with proper objects being
created from the results. The objects are all defined in the `helpscout.models
package <https://laslabs.github.io/python-helpscout/helpscout.models.html>`_.

Web Hooks
---------

`Web Hooks <https://laslabs.github.io/python-helpscout/helpscout.web_hook.html#helpscout.web_hook.web_hook.WebHook>`_
can be received using the ``web_hook`` property on an instantiated `HelpScout
<https://laslabs.github.io/python-helpscout/helpscout.html#helpscout.HelpScout>`_
object, which returns a `WebHookEvent
<https://laslabs.github.io/python-helpscout/helpscout.web_hook.html#helpscout.web_hook.web_hook_event.WebHookEvent>`_
representing the parsed request.

.. code-block:: python

   signature = '2iFmnzC8SCNVF/iNiMnSe19yceU=\n'  # (``X-HelpScout-Signature`` Header)
   event_type = 'customer.created'  # (``X-HelpScout-Event`` Header)
   request_body = '{"firstName":"Jackie","lastName":"Chan",' \
                  '"email":"jackie.chan@somewhere.com",' \
                  '"gender":"male"}'

   event = hs.web_hook(
       event_type, signature, request_body,
   )

The ``WebHookEvent`` that is returned contains two properties:

* ``event_type`` (*str*): The type of event that is being represented
* ``record`` (*helpscout.BaseModel*): The parsed data record for this request

Given the above example:

.. code-block:: python

   >>> event.event_type
   'customer.created'
   >>> event.record
   <helpscout.models.customer.Customer object at 0x101723e50>

Known Issues / RoadMap
======================

* Add better validations (like regexes for emails)
* Verify required attributes, particularly when creating for API instead of
  receiving
* Attachment handling in Conversations (Create/Delete Attachment)
* Raw email source handling in Conversations (Get Thread Source)
* Implement List Customers by Mailbox
* Implement Workflows
* Implement index lookup for the RequestPaginator (currently only response
  iteration is supported)
* Make the domain add syntax more robust (right now AND + OR don't combine well)

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

.. |Build Status| image:: https://img.shields.io/travis/LasLabs/python-helpscout/master.svg
   :target: https://travis-ci.org/LasLabs/python-helpscout
.. |Test Coverage| image:: https://img.shields.io/codecov/c/github/LasLabs/python-helpscout/master.svg
   :target: https://codecov.io/gh/LasLabs/python-helpscout
.. |Code Climate| image:: https://img.shields.io/codeclimate/github/LasLabs/python-helpscout.svg
   :target: https://codeclimate.com/github/LasLabs/python-helpscout
.. |License MIT| image:: https://img.shields.io/github/license/laslabs/python-helpscout.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT
.. |PyPi Package| image:: https://img.shields.io/pypi/v/helpscout.svg
   :target: https://pypi.python.org/pypi/helpscout
   :alt: PyPi Package
.. |PyPi Versions| image:: https://img.shields.io/pypi/pyversions/helpscout.svg
   :target: https://pypi.python.org/pypi/helpscout
   :alt: PyPi Versions
