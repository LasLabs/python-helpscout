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

Images
------

* LasLabs: `Icon <https://repo.laslabs.com/projects/TEM/repos/odoo-module_template/browse/module_name/static/description/icon.svg?raw>`_.

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
