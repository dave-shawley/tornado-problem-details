from __future__ import annotations

import http.client
import typing

from tornado import web


class Problem(web.HTTPError):
    """An exception that will be translated into a json document.

    :param status_code: HTTP status code to return
    :param log_message: optional log message that is passed
        to the :class:`tornado.web.HTTPError` initializer
    :param args: parameters that are passed to `log_message` in
        the :class:`~tornado.web.HTTPError` initializer.
    :keyword str reason: optional reason phrase to use in the
        HTTP response line.  *This value is NOT included in the
        response document*.
    :param kwargs: additional keyword parameters are included in
        the response document

    :meth:`problemdetails.ErrorWriter.write_error` recognizes this
    exception type and renders :attr:`.document` as the *problem+json*
    result.  The *status* property is set to `status_code` and the
    *type* property will be set by ``write_error`` unless it is
    explicitly set.

    .. attribute:: document

       The keyword parameters are collected into this :class:`dict`
       and rendered as the response document

    """

    def __init__(self,
                 status_code: int,
                 log_message: str | None = None,
                 *args: typing.Any,
                 **kwargs: typing.Any) -> None:
        kwargs.setdefault(
            'reason', http.client.responses.get(status_code,
                                                'Abnormal Status'))
        super(Problem, self).__init__(status_code, log_message, *args,
                                      **kwargs)
        self.document = kwargs
        self.document['status'] = status_code
        self.document.pop('reason', None)
        self.document.pop('log_message', None)
