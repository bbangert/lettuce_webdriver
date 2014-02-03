"""
Django-specific extensions
"""

import socket
import urlparse

from lettuce import step
from lettuce.django import server

# make sure the steps are loaded
import lettuce_webdriver.webdriver  # pylint:disable=unused-import


def site_url(url):
    """
    Determine the server URL.
    """
    base_url = 'http://%s' % socket.gethostname()

    if server.port is not 80:
        base_url += ':%d' % server.port

    return urlparse.urljoin(base_url, url)


@step(r'I visit site page "([^"]*)"')
def visit_page(self, page):
    """
    Visit the specific page of the site.
    """

    self.given('I visit "%s"' % site_url(page))
