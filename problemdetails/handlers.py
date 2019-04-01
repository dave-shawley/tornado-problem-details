import json

from tornado import web

from problemdetails import Problem


def _rfc_link(rfc_no, anchor=None):
    if anchor:
        return 'https://tools.ietf.org/html/rfc{0}#{1}'.format(rfc_no, anchor)
    return 'https://tools.ietf.org/html/rfc{0}'.format(rfc_no)


type_link_map = {
    100: _rfc_link(7231, 'section-6.2.1'),
    101: _rfc_link(7231, 'section-6.2.2'),
    200: _rfc_link(7231, 'section-6.3.1'),
    201: _rfc_link(7231, 'section-6.3.2'),
    202: _rfc_link(7231, 'section-6.3.3'),
    203: _rfc_link(7231, 'section-6.3.4'),
    204: _rfc_link(7231, 'section-6.3.5'),
    205: _rfc_link(7231, 'section-6.3.6'),
    206: _rfc_link(7233, 'section-4.1'),
    207: _rfc_link(4918),
    208: _rfc_link(5842),
    226: _rfc_link(3229),
    300: _rfc_link(7231, 'section-6.4.1'),
    301: _rfc_link(7231, 'section-6.4.2'),
    302: _rfc_link(7231, 'section-6.4.3'),
    303: _rfc_link(7231, 'section-6.4.4'),
    305: _rfc_link(7231, 'section-6.4.5'),
    306: _rfc_link(7231, 'section-6.4.6'),
    307: _rfc_link(7231, 'section-6.4.7'),
    308: _rfc_link(7538),
    400: _rfc_link(7231, 'section-6.5.1'),
    401: _rfc_link(7235, 'section-3.1'),
    402: _rfc_link(7231, 'section-6.5.2'),
    403: _rfc_link(7231, 'section-6.5.3'),
    404: _rfc_link(7231, 'section-6.5.4'),
    405: _rfc_link(7231, 'section-6.5.5'),
    406: _rfc_link(7231, 'section-6.5.6'),
    407: _rfc_link(7235, 'section-3.2'),
    408: _rfc_link(7231, 'section-6.5.7'),
    409: _rfc_link(7231, 'section-6.5.8'),
    410: _rfc_link(7231, 'section-6.5.9'),
    411: _rfc_link(7231, 'section-6.5.10'),
    412: _rfc_link(7232, 'section-4.2'),
    413: _rfc_link(7231, 'section-6.5.11'),
    414: _rfc_link(7231, 'section-6.5.12'),
    415: _rfc_link(7231, 'section-6.5.13'),
    416: _rfc_link(7233, 'section-4.4'),
    417: _rfc_link(7231, 'section-6.5.14'),
    421: _rfc_link(7540, 'section-9.1.2'),
    422: _rfc_link(4918),
    423: _rfc_link(4918),
    424: _rfc_link(4918),
    425: _rfc_link(8470),
    426: _rfc_link(7231, 'section-6.5.15'),
    428: _rfc_link(6585),
    429: _rfc_link(6585),
    431: _rfc_link(6585),
    451: _rfc_link(7725),
    500: _rfc_link(7231, 'section-6.6.1'),
    501: _rfc_link(7231, 'section-6.6.2'),
    502: _rfc_link(7231, 'section-6.6.3'),
    503: _rfc_link(7231, 'section-6.6.4'),
    504: _rfc_link(7231, 'section-6.6.5'),
    505: _rfc_link(7231, 'section-6.6.6'),
    506: _rfc_link(2295),
    507: _rfc_link(4918),
    508: _rfc_link(5842),
    510: _rfc_link(2274),
    511: _rfc_link(6585),
}
"""Mapping of HTTP status code to *type* link.

This table maps HTTP status codes to the IANA registered
specification for the code.  You can add additional links or
replace ones that are here as you see fit.  The error writer
uses this table to generate the default ``type`` link in
responses.

"""


class ErrorWriter(web.RequestHandler):
    """Render *application/problem+json* in ``write_error``

    Include this class in the base class list to return errors as
    `application/problem+json`_ documents instead of HTML.

    .. _application/problem+json: https://tools.ietf.org/html/rfc7807

    """

    def write_error(self, status_code, **kwargs):
        """Render *application/problem+json* documents instead of HTML.

        :param int status_code: HTTP status code that we returned
        :keyword str detail: optional *detail* field to include in
            the error document.  This field is omitted by default.
        :keyword str instance: optional *instance* to include in the
            error document.  This field is omitted by default.
        :keyword str title: optional *title* to include in the error
            document.  THis field is omitted by default.
        :keyword str type:  optional *type* field to include in the
            error document.  This field defaults to a link to the
            official HTTP specification of `status_code` if omitted
            and `status_code` is a standard code.

        See :rfc:`7807#section-3.1` for a description of each optional
        field.

        """
        body = {}
        if 'exc_info' in kwargs:
            exc_value = kwargs['exc_info'][1]
            if isinstance(exc_value, Problem):
                body = exc_value.document.copy()

        if not body:
            status_code = int(status_code)
            body = {'status': status_code}
            sentinel = object()
            for kwarg in ('detail', 'instance', 'title', 'type'):
                if kwargs.get(kwarg, sentinel) is not sentinel:
                    body[kwarg] = kwargs[kwarg]

        if 'type' not in body:
            try:
                body['type'] = type_link_map[status_code]
            except KeyError:
                pass

        self.set_header('Content-Type', 'application/problem+json')
        self.write(json.dumps(body).encode('utf-8'))
