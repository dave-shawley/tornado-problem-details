"""
Simple handler that invokes httpbin.org/status.

This file contains a simple handler that sends a request to httpbin.org,
receives an error response (from Tornado), and formats it into a problem
document.  The example handler shows how to catch a HTTPError and
transform it into a problemdetails.Problem.

"""
import asyncio
import logging
import os
import signal

from tornado import httpclient, web
import problemdetails


class HttpBinHandler(problemdetails.ErrorWriter, web.RequestHandler):
    async def get(self):
        logger = logging.getLogger('HttpBinHandler')
        url = 'http://httpbin.org/status/{0}'.format(
            self.get_query_argument('status', '500'))
        logger.info('retrieving %s', url)

        client = httpclient.AsyncHTTPClient()
        try:
            response = await client.fetch(url)
            self.add_header('Content-Type', 'application/json')
            self.write(response.body)
        except httpclient.HTTPError as error:
            raise problemdetails.Problem(
                status_code=error.code,
                httpbin_headers=dict(error.response.headers.items()))


async def main():
    app = web.Application([web.url('/', HttpBinHandler)], debug=True)
    port = int(os.environ.get('PORT', '8000'))
    stem = 'http://127.0.0.1:{0}'.format(port)
    app.listen(address='127.0.0.1', port=port)

    logging.info('listening on %s', stem)
    logging.info('try me at %s?status=500', stem)

    event = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, event.set)
    loop.add_signal_handler(signal.SIGTERM, event.set)
    await event.wait()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(levelname)-8s %(name)s: %(message)s')
    asyncio.run(main())
