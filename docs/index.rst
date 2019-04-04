.. include:: ../README.rst

Examples
========
You can run any of the examples in this section by preparing a Python
environment::

   $ python3 -mvenv env
   $ env/bin/pip install -qe .
   $ env/bin/python examples/httpbin.py
   D - asyncio: Using selector: KqueueSelector
   I - root: listening on http://127.0.0.1:8000
   I - root: GET http://127.0.0.1:8000/?status=419

The examples run the application in *debug mode* so changing the source
code results in the application reloading immediately.  Feel free to
play with the examples.

httpbin.org
-----------
This example sends a request to httpbin.org that generates a HTTP failure.
The failure is caught as a :class:`tornado.web.HTTPError` instance and
translated into a :class:`problemdetails.Problem` instance.  You can run
this example with ``python examples/httpbin.py`` and send requests to
``http://localhost:8000/?status=500``.

.. literalinclude:: ../examples/httpbin.py
   :language: python
   :pyobject: HttpBinHandler.get

RFC-7807 examples
-----------------
This example includes two endpoints that return the examples from :rfc:`7807`.
The first example returns the 403 credit error from section 3.  This example
exemplifies raising an exception where the failure is detected and finishing
the request processing by not catching the exception.  The raised exception
is fairly complex but constructed from literals.

.. literalinclude:: ../examples/rfc7807.py
   :language: python
   :pyobject: AccountHandler

The second example returns the more complex 400 invalid parameter error from
section 3.  The errors are accumulated into a list and raised from the
top-level after the parameters are extracted.  This is a different approach
where all of the error handling is explicit and at the top-level.

.. literalinclude:: ../examples/rfc7807.py
   :language: python
   :pyobject: ValidationError

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

`0.0.5`_ (4 Apr 2019)
---------------------
- Make content type configurable.

`0.0.4`_ (2 Apr 2019)
---------------------
- Made compatible with Python 2.7, Tornado 4.4, Tornado 4.5, & Tornado 5.

`0.0.2`_ (1 Apr 2019)
---------------------
- Add :exc:`problemdetails.Problem`

`0.0.1`_ (31 Mar 2019)
----------------------
- Initial alpha release containing a very simple implementation.

.. _Next Release: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.5...master
.. _0.0.5: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.4...0.0.5
.. _0.0.4: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.2...0.0.4
.. _0.0.2: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.1...0.0.2
.. _0.0.1: https://github.com/dave-shawley/tornado-problem-details/compare/0.0.0...0.0.1
