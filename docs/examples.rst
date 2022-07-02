Examples
========
You can run any of the examples in this section by preparing a Python
environment::

   $ python3 -mvenv env
   $ env/bin/pip install -q '.[examples]'
   $ env/bin/python examples/httpbin.py
   DEBUG     asyncio: Using selector: KqueueSelector
   INFO      root: listening on http://127.0.0.1:8000
   INFO      root: try me at http://127.0.0.1:8000/?status=500

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
This example includes two endpoints that return the examples from :rfc:`7807`:

#. POST http://127.0.0.1:8000/account/1234?price=40
#. GET  http://127.0.0.1:8000/invalid-params
#. GET  http://127.0.0.1:8000/invalid-params?age=-10&color

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

JSON Schema and Open API
------------------------
This example implements a very simple create & retrieve interface that
could be the beginning of a customer data service.  It includes a complete
Open API 3 schema, a documentation endpoint that renders the API, and
JSON schema validation of incoming requests.  Since it is an example,
everything is in one file including the Open API specification, the data
store implementation, and all of the handlers.

#. POST http://127.0.0.1:8000/ to create a new customer
#. GET http://127.0.0.1:8000/<id> to retrieve a customer
#. GET http://127.0.0.1:8000/ to view the API documentation
#. GET http://127.0.0.1:8000/openapi.json for the machine-readable
   specification

The Open API specification is embedded as a long literal YAML string.  It
is deserialized and stored in the application settings so handlers refer
to it using ``self.settings['openapi']``.  The creation handler uses the
JSON schema embedded in the API specification to validate the request
entity and transforms JSON schema validation errors into a readable error
document.

The customer creation handler is the most interesting so let's start there
first.

.. literalinclude:: ../examples/schemified.py
   :language: python
   :pyobject: CreateHandler.post
   :linenos:
   :emphasize-lines: 22-34

Lines 2-10 verify that the incoming request is a JSON entity.  If not, it
generates a `415 Unsupported Media Type`_ response.  Lines 12-20 decode the
incoming request body and generates a `400 Bad Request`_ if it fails to
JSON decode the body.

Lines 22-34 are the interesting ones.  The Open API specification is
available as ``self.settings['openapi']`` and the incoming message schema
is in *components/schemas/CustomerDetails*.  The message schema is used to
validate the incoming request as described in the `python-jsonschema`_
documentation.  :func:`jsonschema.exceptions.best_match` function will
return the *most important* error from ``all_errors`` if the request body
failed to validate.  In the case, a `422 Unprocessable Request`_ is returned
with a lot of detail embedded in the problem document.

If it receives a well-formed JSON document that is lacking information then
it responds with the expected mixture of human-readable and machine-processable
information.

.. code-block:: http

   POST / HTTP/1.1
   Content-Type: application/json; charset=UTF-8
   Host: 127.0.0.1:8000

   {"name":"Dave Shawley","address":{"address":"somewhere"}}

.. code-block:: http

   HTTP/1.1 422 Unprocessable Entity
   Content-Length: 426
   Content-Type: application/problem+json
   Date: Mon, 08 Apr 2019 13:36:15 GMT
   Server: TornadoServer/6.0.2

   {
       "detail": "'email' is a required property",
       "failure": [
           {
               "absolute_path": [
                   "address"
               ],
               "absolute_schema_path": [
                   "properties",
                   "address",
                   "required"
               ],
               "context": [],
               "message": "'country' is a required property"
           },
           {
               "absolute_path": [],
               "absolute_schema_path": [
                   "required"
               ],
               "context": [],
               "message": "'email' is a required property"
           }
       ],
       "status": 422,
       "title": "Failed to process request",
       "type": "/errors#jsonschema-failure"
   }

The last piece that requires some explanation is the slight customization
to the JSON encoder.  A custom "default object handler" is installed into
the error writer's JSON encoder.  The object handler is shown below.  It
knows how to translate :exc:`~jsonschema.exceptions.ValidationError`
instances into readable documents.

.. literalinclude:: ../examples/schemified.py
   :language: python
   :pyobject: jsonify
   :emphasize-lines: 5-11

The JSON document generation is customized by setting the ``default``
attribute on the :any:`problemdetails.ErrorWriter.json_encoder` instance
when the application is created.

.. literalinclude:: ../examples/schemified.py
   :language: python
   :pyobject: main
   :emphasize-lines: 14-16

.. _python-jsonschema: https://python-jsonschema.readthedocs.io/en/stable
   /errors/#best-match-and-relevance
.. _400 Bad Request: https://tools.ietf.org/html/rfc7231#section-6.5.1
.. _415 Unsupported Media Type: https://tools.ietf.org/html/rfc7231
   #section-6.5.13
.. _422 Unprocessable Request: https://tools.ietf.org/html/rfc4918#section-11.2
