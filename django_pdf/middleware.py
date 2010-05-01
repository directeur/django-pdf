#!/usr/bin/env python

import os.path
import cStringIO as StringIO
import cgi
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.http import HttpResponse
from django.conf import settings

REQUEST_FORMAT_NAME = getattr(settings, 'REQUEST_FORMAT_NAME', 'format')
REQUEST_FORMAT_PDF_VALUE = getattr(settings, 'REQUEST_FORMAT_PDF_VALUE', 'pdf')
TEMPLATE_PDF_CHECK = getattr(settings, 'TEMPLATE_PDF_CHECK',
'DJANGO_PDF_OUTPUT')


def fetch_resources(uri, rel):
    """
    Prepares paths for pisa
    """
    path = os.path.join(settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, ""))
    return path


def transform_to_pdf(response):
    response['mimetype'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename=report.pdf'
    content = response.content
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(content),
            response, link_callback=fetch_resources)
    if not pdf.err:
        return response
    else:
        return http.HttpResponse('We had some errors<pre>%s</pre>' %
                cgi.escape(html))


class PdfMiddleware(object):
    """
    Converts the response to a pdf one.
    """
    def process_response(self, request, response):
        format = request.GET.get(REQUEST_FORMAT_NAME, None)
        if format == REQUEST_FORMAT_PDF_VALUE:
            response = transform_to_pdf(response)
        return response
