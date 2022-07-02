"""Pair of handlers that implement the examples from :rfc:`7807`."""
import asyncio
import logging
import os
import signal

from tornado import web
import problemdetails


class AccountHandler(problemdetails.ErrorWriter, web.RequestHandler):
    def post(self, account):
        price = float(self.get_query_argument('price'))
        self.verify_funds(account, price)
        self.buy_thing()

    def verify_funds(self, account, price):
        balance = self.get_balance(account)
        if price > balance:
            raise problemdetails.Problem(
                status_code=403,
                title='You do not have enough credit.',
                detail=(f'Your current balance is {balance}, but that '
                        f'costs {price}'),
                instance=self.reverse_url('account-handler', account),
                balance=balance,
                accounts=self.lookup_accounts(account),
                type='https://example.com/probs/out-of-credit',
            )

    def get_balance(self, account):
        return 30.0  # TODO look up balance

    def lookup_accounts(self, primary_account):
        related = [12345, 67890]  # TODO lookup related accounts
        return [self.reverse_url('account-handler', aid) for aid in related]

    def buy_thing(self):
        pass


class ValidationError(problemdetails.ErrorWriter, web.RequestHandler):
    def initialize(self):
        super(ValidationError, self).initialize()
        self.errors = []

    def get(self):
        age = self._extract_age()
        color = self._extract_color()
        if self.errors:
            raise problemdetails.Problem(**{
                'status_code': 400,
                'type': 'https://example.net/validation-error',
                'invalid-params': self.errors,
            })
        self.write({'age': age, 'color': color})

    def _record_error(self, field, error):
        self.errors.append({'name': field, 'reason': error})

    def _extract_age(self):
        try:
            age = self.get_query_argument('age')
        except web.MissingArgumentError:
            self._record_error('age', 'is required')
        else:
            try:
                age = int(age)
                if age > 0:
                    return age
                self._record_error('age', 'must be a positive integer')
            except ValueError:
                self._record_error('age', 'must be a integer')
        return None

    def _extract_color(self):
        try:
            color = self.get_query_argument('color')
        except web.MissingArgumentError:
            self._record_error('color', 'is required')
        else:
            if color in ('blue', 'green', 'red'):
                return color
            self._record_error('color', "must be 'green', 'red' or 'blue'")
        return None


async def main():

    app = web.Application([
        web.url(r'/account/(?P<account>\d+)', AccountHandler,
                name='account-handler'),
        web.url(r'/invalid-params', ValidationError),
    ], debug=True)

    port = int(os.environ.get('PORT', '8000'))
    stem = 'http://127.0.0.1:{0}'.format(port)
    app.listen(address='127.0.0.1', port=port)

    logging.info('listening on %s', stem)
    logging.info('try the following:')
    logging.info('POST %s/account/1234?price=40', stem)
    logging.info('GET  %s/invalid-params', stem)
    logging.info('GET  %s/invalid-params?age=-10&color', stem)

    event = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, event.set)
    loop.add_signal_handler(signal.SIGTERM, event.set)
    await event.wait()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(levelname)1.1s - %(name)s: %(message)s')
    asyncio.run(main())
