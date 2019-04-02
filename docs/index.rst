.. include:: ../README.rst

Reference
=========
.. autoclass:: problemdetails.ErrorWriter
   :members:

.. autoclass:: problemdetails.Problem
   :members:

.. data:: problemdetails.type_link_map

   Mapping of HTTP status code to *type* link.

   This table maps HTTP status codes to the IANA registered
   specification for the code.  You can add additional links or
   replace ones that are here as you see fit.  The error writer
   uses this table to generate the default ``type`` link in
   responses.

Release History
===============

`0.0.3`_ (2 Apr 2019)
---------------------
- Made compatible with Python 2.7, Tornado 4.4, Tornado 4.5, & Tornado 5.

`0.0.2`_ (1 Apr 2019)
---------------------
- Add :exc:`problemdetails.Problem`

`0.0.1`_ (31 Mar 2019)
----------------------
- Initial alpha release containing a very simple implementation.

.. _0.0.2: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.1...0.0.2
.. _0.0.1: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.0...0.0.1
