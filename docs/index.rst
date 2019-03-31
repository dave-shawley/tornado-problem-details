.. include:: ../README.rst

Reference
=========
.. autoclass:: problemdetails.ErrorWriter
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

`0.0.1`_ (31 Mar 2019)
----------------------
- Initial alpha release containing a very simple implementation.

.. _0.0.1: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.0...0.0.1
