RFC-7807 implementation for Tornado
===================================
|build| |coverage| |docs| |download| |license| |source|

This library provides a version of ``tornado.web.RequestHandler.send_error``
that speaks ``application/problem+json`` instead of HTML.

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
