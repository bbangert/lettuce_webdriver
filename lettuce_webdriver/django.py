"""
Django-specific extensions
"""


def site_url(url):
    """
    Determine the server URL.
    """
    base_url = 'http://%s' % socket.gethostname()

    if server.port is not 80:
        base_url += ':%d' % server.port

    return urlparse.urljoin(base_url, url)


@step(r'I visit site page "([^"]*)"')
def visit_page(step, page):
    """
    Visit the specific page of the site.
    """

    step.given('I visit "%s"' % site_url(page))
