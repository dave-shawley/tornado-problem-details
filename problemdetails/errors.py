from tornado import web


class Problem(web.HTTPError):
    """An exception that will be translated into a json document.

    :param int status_code: HTTP status code to return
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

    def __init__(self, status_code, *args, **kwargs):
        super().__init__(status_code, *args, **kwargs)
        self.document = kwargs
        self.document['status'] = status_code
