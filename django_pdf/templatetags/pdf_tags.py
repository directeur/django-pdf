from django import template
from django.http import Http404
from django.conf import settings

register = template.Library()

REQUEST_FORMAT_NAME = getattr(settings, 'REQUEST_FORMAT_NAME', 'format')
REQUEST_FORMAT_PDF_VALUE = getattr(settings, 'REQUEST_FORMAT_PDF_VALUE', 'pdf')
TEMPLATE_PDF_CHECK = getattr(settings, 'TEMPLATE_PDF_CHECK',
'DJANGO_PDF_OUTPUT')


def pdf_link(parser, token):
    """
    Parses a tag that's supposed to be in this format: {% pdf_link title %}
    """
    bits = [b.strip('"\'') for b in token.split_contents()]
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "pdf_link tag takes 1 argument"
    title = bits[1]
    return PdfLinkNode(title.strip())


class PdfLinkNode(template.Node):
    """
    Renders an <a> HTML tag with a link which href attribute
    includes the ?REQUEST_FORMAT_NAME=REQUEST_FORMAT_PDF_VALUE
    to the current page's url to generate a PDF link to the PDF version of this
    page.

    Eg.
        {% pdf_link PDF %} generates
        <a href="/the/current/path/?format=pdf" title="PDF">PDF</a>

    """
    def __init__(self, title):
        self.title = title

    def render(self, context):
        request = context['request']
        getvars = request.GET.copy()
        getvars[REQUEST_FORMAT_NAME] = REQUEST_FORMAT_PDF_VALUE

        if len(getvars.keys()) > 1:
            urlappend = "&%s" % getvars.urlencode()
        else:
            urlappend = '%s=%s' % (REQUEST_FORMAT_NAME, REQUEST_FORMAT_PDF_VALUE)

        url = '%s?%s' % (request.path, urlappend)
        return '<a href="%s" title="%s">%s</a>' % (url, self.title, self.title)

pdf_link = register.tag(pdf_link)
