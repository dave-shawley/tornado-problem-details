"""
Simple handler that invokes httpbin.org/status.

This file contains a simple handler that sends a request to httpbin.org,
receives an error response (from Tornado), and formats it into a problem
document.  The example handler shows how to catch a HTTPError and
transform it into a problemdetails.Problem.

"""
import logging
import os

from tornado import gen, httpclient, ioloop, web
import problemdetails


class HttpBinHandler(problemdetails.ErrorWriter, web.RequestHandler):
    @gen.coroutine
    def get(self):
        logger = logging.getLogger('HttpBinHandler')
        url = 'http://httpbin.org/status/{0}'.format(
            self.get_query_argument('status', '500'))
        logger.info('retrieving %s', url)

        client = httpclient.AsyncHTTPClient()
        try:
            response = yield client.fetch(url)
            self.add_header('Content-Type', 'application/json')
            self.write(response.body)
        except httpclient.HTTPError as error:
            raise problemdetails.Problem(
                status_code=error.code,
                httpbin_headers=dict(error.response.headers.items()))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(levelname)1.1s - %(name)s: %(message)s')
    app = web.Application([web.url('/', HttpBinHandler)], debug=True)

    iol = ioloop.IOLoop.current()
    port = int(os.environ.get('PORT', '8000'))
    stem = 'http://127.0.0.1:{0}'.format(port)
    logging.info('listening on %s', stem)
    logging.info('GET %s/?status=418', stem)

    app.listen(address='127.0.0.1', port=port)
    try:
        iol.start()
    except KeyboardInterrupt:
        iol.stop()
