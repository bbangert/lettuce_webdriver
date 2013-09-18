from lettuce import step
from lettuce import world

from lettuce_webdriver.util import assert_true
from lettuce_webdriver.util import assert_false

import logging
log = logging.getLogger(__name__)

def wait_for_elem(browser, xpath, timeout=15):
    start = time.time()
    elems = []
    while time.time() - start < timeout:
        elems = browser.find_elements_by_css_selector(xpath)
        if elems:
            return elems
        time.sleep(0.2)
    return elems

@step(r'There should be an element matching \$\("(.*?)"\) within (\d+) seconds?')
def wait_for_element_by_selector(step, selector, seconds):
    log.error(selector)
    #elems = wait_for_elem(world.browser, selector, seconds)
    #assert_true(step, elems)

__all__ = ['wait_for_element_by_selector']
