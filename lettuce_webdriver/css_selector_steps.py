import time

from lettuce import step
from lettuce import world

from lettuce_webdriver.util import assert_true
from lettuce_webdriver.util import assert_false

import logging
log = logging.getLogger(__name__)

def wait_for_elem(browser, sel, timeout=15):
    start = time.time()
    elems = []
    while time.time() - start < timeout:
        elems = browser.find_elements_by_css_selector(sel)
        if elems:
            return elems
        time.sleep(0.2)
    return elems

@step(r'There should be an element matching \$\("(.*?)"\) within (\d+) seconds?$')
def wait_for_element_by_selector(step, selector, seconds):
    elems = wait_for_elem(world.browser, selector, seconds)
    assert_true(step, elems)


@step(r'I fill in \$\("(.*?)"\) with "(.*?)"$')
def fill_in_by_selector(step, selector, value):
    elem = world.browser.find_element_by_css_selector(selector)
    elem.clear()
    elem.send_keys(value)


@step(r'I submit \$\("(.*?)"\)')
def submit_by_selector(step, selector):
    elem = world.browser.find_element_by_css_selector(selector)
    elem.submit()


@step(r'I check \$\("(.*?)"\)$')
def check_by_selector(step, selector):
    elem = world.browser.find_element_by_css_selector(selector)
    if not elem.is_selected():
        elem.click()


__all__ = [
    'wait_for_element_by_selector',
    'fill_in_by_selector',
    'check_by_selector',
]
