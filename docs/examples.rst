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
