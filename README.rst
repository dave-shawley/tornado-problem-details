RFC-7807 implementation for Tornado
===================================
|build| |coverage| |docs| |download| |license| |source|

This library provides a version of ``tornado.web.RequestHandler.send_error``
that speaks ``application/problem+json`` instead of HTML.  The easiest
way to use this library is to inherit from ``problemdetails.ErrorWriter``
and call ``send_error()`` with additional parameters.

.. code-block:: python

   from tornado import web
   import problemdetails


   class MyHandler(problemdetails.ErrorWriter, web.RequestHandler):
      def get(self):
         try:
            self.do_something_hard()
         except SomeException as error:
            self.send_error(500, title="Failed to do_something_hard")

.. code-block:: http

   HTTP/1.1 500 Internal Server Error
   Content-Type: application/problem+json

   {
      "title": "Failed to do_something_hard",
      "type": "https://tools.ietf.org/html/rfc7231#section-6.6.1"
   }

As an alternative, you can raise a ``problemdetails.Problem`` instance and let
the Tornado exception handling take care of eventually calling ``write_error``.
The following snippet produces the same output as the previous example.

.. code-block:: python

   from tornado import web
   import problemdetails


   class MyHandler(problemdetails.ErrorWriter, web.RequestHandler):
      def get(self):
         if not self.do_something_hard():
            raise problemdetails.Problem(status_code=500,
                                         title='Failed to do_something_hard')

The ``problemdetails.Problem`` instance passes all of the keyword parameters
through in the resulting message so it is very easy to add fields.  The
interface of ``tornado.web.RequestHandler.send_error`` is less expressive
since keyword parameters may be swallowed by intervening code.

.. |build| image:: https://img.shields.io/circleci/project/github/dave-shawley/tornado-problem-details/master.svg?style=social
   :target: https://circleci.com/gh/dave-shawley/tornado-problem-details/tree/master
.. |coverage| image:: https://img.shields.io/coveralls/github/dave-shawley/tornado-problem-details.svg?style=social
   :target: https://coveralls.io/github/dave-shawley/tornado-problem-details?branch=master
.. |docs| image:: https://img.shields.io/readthedocs/tornado-problem-details.svg?style=social
   :target: https://tornado-problem-details.readthedocs.io/en/latest/?badge=latest
.. |download| image:: https://img.shields.io/pypi/pyversions/tornado-problem-details.svg?style=social
   :target: https://pypi.org/project/tornado-problem-details/
.. |license| image:: https://img.shields.io/pypi/l/tornado-problem-details.svg?style=social
   :target: https://github.com/dave-shawley/tornado-problem-details/blob/master/LICENSE.txt
.. |source| image:: https://img.shields.io/badge/source-github.com-green.svg?style=social
   :target: https://github.com/dave-shawley/tornado-problem-details
