"""
Fairly complex example of using json-schema and problem+json together.

This example implements a very simple create & retrieve interface that
could be the beginning of a customer data service.  Since it is an example,
everything is in this file including the Open API specification, the data
store implementation, and all of the handlers.

POST /
    to create a new customer
GET /<id>
    to retrieve a customer
GET /
    to view the API documentation
GET /openapi.json
    for the machine-readable specification

The Open API specification is embedded as a long literal YAML string.  It
is deserialized and stored in the application settings so handlers refer
to it using ``self.settings['openapi']``.  The creation handler uses the
JSON schema embedded in the API specification to validate the request
entity and transforms JSON schema validation errors into a readable error
document.

"""
import asyncio
import cgi
import copy
import logging
import json
import os
import signal
import uuid

from tornado import web
import jsonschema.exceptions
import problemdetails
import yaml

OPENAPI_SCHEMA = '''
openapi: "3.0.2"
info:
  title: "Customer API"
  version: "1.0"
paths:
  /:
    post:
      summary: "Create a new customer"
      operationId: "createCustomer"
      requestBody:
        description: "Customer details"
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CustomerDetails"
        required: true
      responses:
        "303":
          description: "Redirect to the newly created customer"
          headers:
            Location:
              description: "Canonical URL for the created customer"
              schema:
                type: string
                format: url
  /{customerId}:
    get:
      summary: "Retrieve a customer"
      operationId: "getCustomer"
      responses:
        "200":
          description: "Requested customer details"
          content:
            application/json:
              schema:
                allOf:
                  - $ref: "#/components/schemas/CustomerID"
                  - $ref: "#/components/schemas/CustomerDetails"
        "404":
          description: |
            <a name="error-customer-does-not-exist">Customer does not exist</a>
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/ProblemDocument"
              example:
                title: "Customer does not exist"
                type: "/errors#customer-does-not-exist"
                status_code: 404
                instance: "/1234"
components:
  schemas:
    CustomerID:
      type: object
      properties:
        id:
          type: string
      required:
        - "id"
    CustomerDetails:
      type: object
      properties:
        name:
          type: string
        date_of_birth:
          type: string
          format: date
        email:
          type: string
          format: email
        address:
          type: object
          properties:
            address:
              type: string
            city:
              type: string
            region:
              type: string
            country:
              type: string
            location_code:
              type: string
          required:
            - address
            - country
      required:
        - email
        - address
    ProblemDocument:
      type: object
      properties:
        status_code:
          description: HTTP status code
          type: integer
          minimum: 100
          maximum: 600
          exclusiveMaximum: true
        type:
          description: Canonical name for this error
          type: string
          format: url
        title:
          description: Human readable description of the failure
          type: string
        instance:
          description: Optional instance URL
          type: string
          format: url
        detail:
          description: Additional details about the failure
          type: string
        failure:
          description: Structured details about the failure
          type: object
      required:
        - status_code
        - type
        - title
servers:
  - url: "http://api.example.com/"
'''


def jsonify(obj):
    """Transform `obj` into something that the JSON encoder can handle."""
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, jsonschema.ValidationError):
        return {
            'absolute_path': list(obj.absolute_path),
            'absolute_schema_path': list(obj.absolute_schema_path),
            'context': obj.context,
            'message': obj.message,
        }
    if isinstance(obj, Exception):
        return {
            'exception': obj.__class__.__name__,
            'message': str(obj),
            'arguments': obj.args,
        }
    raise TypeError('{0} is not JSON serializable'.format(
        obj.__class__.__name__))


class CustomerDatabase:
    """In-memory data store."""

    def __init__(self):
        self._records = {}

    def insert(self, record):
        record_id = str(uuid.uuid4())
        self._records[record_id] = copy.deepcopy(record)
        self._records[record_id]['id'] = record_id
        return record_id

    def fetch(self, record_id):
        return self._records.get(record_id, None)


class CreateHandler(problemdetails.ErrorWriter, web.RequestHandler):
    """Create a new customer record."""

    def get(self):
        # Tornado doesn't make GET and POST handlers in separate
        # classes sharing the same path easy so I'll just redirect
        self.redirect(self.reverse_url('docs'))

    def post(self):
        content_type, params = cgi.parse_header(
            self.request.headers.get('Content-Type', 'application/json'))
        if content_type != 'application/json':
            raise problemdetails.Problem(
                status_code=415,
                title='Content type is not understood',
                detail='Cannot decode {0}, try application/json'.format(
                    content_type),
            )

        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except (TypeError, ValueError, UnicodeDecodeError) as error:
            raise problemdetails.Problem(
                status_code=400,
                title='Failed to decode request',
                detail=str(error),
                failure=error,
            )

        openapi = self.settings['openapi']
        validator = jsonschema.Draft7Validator(
            schema=openapi['components']['schemas']['CustomerDetails'])
        all_errors = list(validator.iter_errors(body))
        most_important = jsonschema.exceptions.best_match(all_errors)
        if most_important is not None:
            raise problemdetails.Problem(
                status_code=422,
                type='/errors#jsonschema-failure',
                title='Failed to process request',
                detail=most_important.message,
                failure=all_errors,
            )

        record_id = self.settings['database'].insert(body)
        self.redirect(self.reverse_url('retrieve', record_id), status=303)


class FetchHandler(problemdetails.ErrorWriter, web.RequestHandler):
    """Retrieve a customer."""

    def get(self, record_id):
        record = self.settings['database'].fetch(record_id)
        if record is None:
            raise problemdetails.Problem(
                status_code=404,
                type='/errors#error-customer-does-not-exist',
                title='Customer {0} does not exist'.format(record_id),
                instance=self.reverse_url('retrieve', record_id),
            )

        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.write(self.settings['json-encoder'].encode(record))


class DocumentationHandler(problemdetails.ErrorWriter, web.RequestHandler):
    """Use redoc to format the Open API specification."""

    def get(self):
        self.set_header('Content-Type', 'text/html')
        self.set_status(200)
        self.write('''
            <!DOCTYPE html><html><head><title>API Documentation</title>
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family={font}"
             rel="stylesheet"><style>body {{margin:0; padding:0}}</style>
            </head><body><redoc spec-url='{openapi}'></redoc>
            <script src="{redoc}"> </script></body></html>
        '''.format(
            font='Montserrat:300,400,700|Roboto:300,400,700',
            redoc=('https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.4/bundles'
                   '/redoc.standalone.js'),
            openapi=self.reverse_url('openapi'),
        ))


class OpenAPIHandler(problemdetails.ErrorWriter, web.RequestHandler):
    """Return the machine-readable Open API specification."""

    def get(self):
        doc = self.settings['openapi']
        doc['servers'] = [{
            'url': self.request.protocol + '://' + self.request.host}]
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.write(self.settings['json-encoder'].encode(doc))


async def main():
    app = web.Application([
        web.url(r'/index.html', DocumentationHandler, name='docs'),
        web.url(r'/openapi.json', OpenAPIHandler, name='openapi'),
        web.url(r'/', CreateHandler, name='create'),
        web.url(r'/(?P<record_id>.+)', FetchHandler, name='retrieve'),
    ])

    app.settings['database'] = CustomerDatabase()
    app.settings['debug'] = True
    app.settings['json-encoder'] = json.JSONEncoder(default=jsonify)
    app.settings['openapi'] = yaml.safe_load(OPENAPI_SCHEMA)

    # Update the error writer's JSON encoder so that it knows
    # how to handle validation errors
    problemdetails.ErrorWriter.json_encoder.default = jsonify

    port = int(os.environ.get('PORT', '8000'))
    app.listen(address='127.0.0.1', port=port)

    event = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, event.set)
    loop.add_signal_handler(signal.SIGTERM, event.set)
    await event.wait()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(levelname)1.1s %(name)s: %(message)s')

    asyncio.run(main())
