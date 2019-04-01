import json
import urllib.parse

from tornado import testing, web

import problemdetails.handlers


class Application(web.Application):
    def __init__(self, **settings):
        super().__init__([web.url('/', Handler)], settings)


class Handler(problemdetails.ErrorWriter, web.RequestHandler):
    def get(self):
        sentinel = object()  # safely detect missing query params

        status = int(self.get_query_argument('status', default='200'))
        raise_error = self.get_query_argument('raise_error', default=sentinel)

        if raise_error is not sentinel:
            query_args = [
                arg for arg in self.request.query_arguments.keys()
                if arg not in ('raise_error', 'status')
            ]
            kwargs = {}
            for name in query_args:
                kwargs[name] = self.get_query_argument(name)
                if kwargs[name].lower() == 'none':
                    kwargs[name] = None
                elif kwargs[name].startswith(('{', '[')):
                    kwargs[name] = json.loads(kwargs[name])
            raise problemdetails.Problem(status_code=status, **kwargs)
        else:
            kwargs = {}
            for name in ('detail', 'instance', 'title', 'type'):
                value = self.get_query_argument(name, sentinel)
                if value is not sentinel:
                    if value.lower() == 'none':
                        value = None
                    kwargs[name] = value
            self.send_error(status, **kwargs)


class ErrorWriterTests(testing.AsyncHTTPTestCase):
    def get_app(self):
        return Application()

    def send_query(self, **query):
        return self.fetch('/?{0}'.format(urllib.parse.urlencode(query)))

    def test_that_send_error_sets_content_type(self):
        response = self.send_query(status=500)
        self.assertEqual(response.code, 500)
        self.assertEqual(response.headers['Content-Type'],
                         'application/problem+json')

    def test_that_send_error_includes_status(self):
        response = self.send_query(status=500)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['status'], 500)

    def test_that_send_error_sets_type_to_rfc_url(self):
        response = self.send_query(status=500)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['type'],
                         problemdetails.handlers.type_link_map[response.code])
        self.assertEqual(body['type'],
                         'https://tools.ietf.org/html/rfc7231#section-6.6.1')

    def test_that_type_is_not_set_for_unknown_status_code(self):
        response = self.send_query(status=600)
        self.assertEqual(response.code, 600)
        body = json.loads(response.body.decode('utf-8'))
        self.assertNotIn('type', body)

    def test_that_type_can_be_overridden(self):
        response = self.send_query(
            status=500, type='http://example.com/errors#500')
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['type'], 'http://example.com/errors#500')

    def test_that_title_can_be_set(self):
        response = self.send_query(status=500, title='Uh oh')
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['title'], 'Uh oh')

    def test_that_instance_can_be_set(self):
        response = self.send_query(
            status=500, instance='http://example.com/probs/out-of-credit')
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['instance'],
                         'http://example.com/probs/out-of-credit')

    def test_that_detail_can_be_set(self):
        response = self.send_query(status=500, detail='something bad happened')
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['detail'], 'something bad happened')

    def test_that_instance_can_be_null(self):
        response = self.send_query(status=500, instance=None)
        body = json.loads(response.body.decode('utf-8'))
        self.assertIsNone(body['instance'], repr(body))


class ProblemTests(ErrorWriterTests):
    def get_app(self):
        return Application()

    def send_query(self, **query):
        query['raise_error'] = True
        return self.fetch('/?{0}'.format(urllib.parse.urlencode(query)))

    def test_that_custom_attributes_can_be_set(self):
        response = self.send_query(
            status=401, custom=json.dumps({'a': ['list']}))
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body['custom'], {'a': ['list']}, repr(body['custom']))
