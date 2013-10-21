import time

from lettuce import step
from lettuce import world

from lettuce_webdriver.util import assert_true
from lettuce_webdriver.util import assert_false

from selenium.common.exceptions import WebDriverException

import logging
log = logging.getLogger(__name__)

def wait_for_elem(browser, sel, timeout=15):
    start = time.time()
    elems = []
    while time.time() - start < timeout:
        elems = find_elements_by_jquery(browser, sel)
        if elems:
            return elems
        time.sleep(0.2)
    return elems


def load_script(browser, url):
    """Ensure that JavaScript at a given URL is available to the browser."""
    browser.execute_script("""
    var script_tag = document.createElement("script");
    script_tag.setAttribute("type", "text/javascript");
    script_tag.setAttribute("src", arguments[0]);
    document.getElementsByTagName("head")[0].appendChild(script_tag);
    """, url)


def find_elements_by_jquery(browser, selector):
    """Find HTML elements using jQuery-style selectors.
    
    Ensures that jQuery is available to the browser; if it gets a
    WebDriverException that looks like """
    try:
        return browser.execute_script("""return $(arguments[0]).get();""", selector)
    except WebDriverException as e:
        if e.msg.startswith(u'$ is not defined'):
            load_script(browser, "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js")
            return browser.execute_script("""return $(arguments[0]).get();""", selector)
        else:
            raise


@step(r'There should be an element matching \$\("(.*?)"\)$')
def check_element_by_selector(step, selector):
    elems = find_elements_by_jquery(world.browser, selector)
    assert_true(step, elems)


@step(r'There should be an element matching \$\("(.*?)"\) within (\d+) seconds?$')
def wait_for_element_by_selector(step, selector, seconds):
    elems = wait_for_elem(world.browser, selector, int(seconds))
    assert_true(step, elems)


@step(r'I fill in \$\("(.*?)"\) with "(.*?)"$')
def fill_in_by_selector(step, selector, value):
    elem = find_elements_by_jquery(world.browser, selector)[0]
    elem.clear()
    elem.send_keys(value)


@step(r'I submit \$\("(.*?)"\)')
def submit_by_selector(step, selector):
    elem = find_elements_by_jquery(world.browser, selector)[0]
    elem.submit()


@step(r'I check \$\("(.*?)"\)$')
def check_by_selector(step, selector):
    elem = find_elements_by_jquery(world.browser, selector)[0]
    if not elem.is_selected():
        elem.click()


@step(r'I click \$\("(.*?)"\)$')
def click_by_selector(step, selector):
    # No need for separate button press step with selector style.
    elem = find_elements_by_jquery(world.browser, selector)[0]
    elem.click()


@step(r'I follow the link \$\("(.*?)"\)$')
def click_by_selector(step, selector):
    elem = find_elements_by_jquery(world.browser, selector)[0]
    href = elem.get_attribute('href')
    world.browser.get(href)


@step(r'\$\("(.*?)"\) should be selected$')
def click_by_selector(step, selector):
    # No need for separate button press step with selector style.
    elem = find_elements_by_jquery(world.browser, selector)[0]
    assert_true(step, elem.is_selected())


__all__ = [
    'wait_for_element_by_selector',
    'fill_in_by_selector',
    'check_by_selector',
    'click_by_selector',
    'check_element_by_selector',
]
