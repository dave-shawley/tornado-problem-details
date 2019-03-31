RFC-7807 implementation for Tornado
===================================
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
