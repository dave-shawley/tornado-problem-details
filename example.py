import json
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
            logger.info('response %r', error.response)
            raise problemdetails.Problem(
                status_code=error.code,
                httpbin_headers=dict(error.response.headers.items()))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)1.1s - %(name)s: %(message)s')
    app = web.Application([web.url('/', HttpBinHandler)], debug=True)
    app.listen(int(os.environ.get('PORT', '8000')))
    iol = ioloop.IOLoop.current()
    try:
        iol.start()
    except KeyboardInterrupt:
        iol.stop()
