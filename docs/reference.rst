Reference
=========
.. autoclass:: problemdetails.ErrorWriter
   :members:

.. autoclass:: problemdetails.Problem
   :members:

.. data:: problemdetails.type_link_map

   Mapping of HTTP status code to *type* link.

   This table maps HTTP status codes to the IANA registered
   specification for the code.  You can add additional links or
   replace ones that are here as you see fit.  The error writer
   uses this table to generate the default ``type`` link in
   responses.
