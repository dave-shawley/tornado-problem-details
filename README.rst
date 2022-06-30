RFC-7807 implementation for Tornado
===================================
|build| |coverage| |docs| |download| |license| |source|

This library provides a version of ``tornado.web.RequestHandler.send_error``
that speaks ``application/problem+json`` instead of HTML.  The easiest
way to use this library is to inherit from ``problemdetails.ErrorWriter``
and raise ``problemdetails.Problem`` exceptions instead of ``HTTPError``.

.. code-block:: python

   class MyHandler(problemdetails.ErrorWriter, web.RequestHandler):
      def get(self):
         if not self.do_something_hard():
            raise problemdetails.Problem(status_code=500,
                                         title='Failed to do_something_hard')

.. code-block:: http

   HTTP/1.1 500 Internal Server Error
   Content-Type: application/problem+json

   {
      "status": 500,
      "title": "Failed to do_something_hard",
      "type": "https://tools.ietf.org/html/rfc7231#section-6.6.1"
   }

You can easily construct more substantial response documents by passing
additional keyword parameters to the ``problemdetails.Problem``
initializer.  They become top-level properties in the response document.

You can also call ``send_error`` directly and produce a response docuemnt.
The following snippet produces the same output as the previous snippet.

.. code-block:: python

   class MyHandler(problemdetails.ErrorWriter, web.RequestHandler):
      def get(self):
         try:
            self.do_something_hard()
         except SomeException as error:
            self.send_error(500, title="Failed to do_something_hard")

The interface of ``tornado.web.RequestHandler.send_error`` is less expressive
since keyword parameters may be swallowed by intervening code.  The only
parameters that are recognized are: ``instance``, ``title``, and ``type``.
Use the exception-based interface for more substantial documents.

.. |build| image:: https://img.shields.io/github/workflow/status/dave-shawley/tornado-problem-details/Testing?style=social
   :target: https://github.com/dave-shawley/tornado-problem-details/actions
.. |coverage| image:: https://img.shields.io/codecov/c/github/dave-shawley/tornado-problem-details?style=social
   :target: https://app.codecov.io/gh/dave-shawley/tornado-problem-details
.. |docs| image:: https://img.shields.io/readthedocs/tornado-problem-details.svg?style=social
   :target: https://tornado-problem-details.readthedocs.io/en/latest/?badge=latest
.. |download| image:: https://img.shields.io/pypi/pyversions/tornado-problem-details.svg?style=social
   :target: https://pypi.org/project/tornado-problem-details/
.. |license| image:: https://img.shields.io/pypi/l/tornado-problem-details.svg?style=social
   :target: https://github.com/dave-shawley/tornado-problem-details/blob/main/LICENSE.txt
.. |source| image:: https://img.shields.io/badge/source-github.com-green.svg?style=social
   :target: https://github.com/dave-shawley/tornado-problem-details
