"""Webdriver support for lettuce"""
import time

from lettuce import step, world

from lettuce_webdriver.util import (assert_true,
                                    assert_false,
                                    AssertContextManager,
                                    find_button,
                                    find_field,
                                    find_option,
                                    option_in_select)

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    NoAlertPresentException,
    WebDriverException)

from nose.tools import assert_equals

# pylint:disable=missing-docstring,redefined-outer-name

from css_selector_steps import *


def contains_content(browser, content):
    # Search for an element that contains the whole of the text we're looking
    #  for in it or its subelements, but whose children do NOT contain that
    #  text - otherwise matches <body> or <html> or other similarly useless
    #  things.
    for elem in browser.find_elements_by_xpath(str(
            '//*[contains(normalize-space(.),"{content}") '
            'and not(./*[contains(normalize-space(.),"{content}")])]'
            .format(content=content))):

        try:
            if elem.is_displayed():
                return True
        except StaleElementReferenceException:
            pass

    return False


def wait_for_elem(browser, xpath, timeout=15):
    start = time.time()
    elems = []
    while time.time() - start < timeout:
        elems = browser.find_elements_by_xpath(str(xpath))
        if elems:
            return elems
        time.sleep(0.2)
    return elems


def wait_for_content(step, browser, content, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        if contains_content(world.browser, content):
            return
        time.sleep(0.2)
    assert_true(step, contains_content(world.browser, content))


## URLS
@step('I visit "(.*?)"$')
def visit(step, url):
    with AssertContextManager(step):
        world.browser.get(url)


@step('I go to "(.*?)"$')
def goto(step, url):
    step.given('I visit "%s"' % url)


## Links
@step('I click "(.*?)"$')
def click(step, name):
    with AssertContextManager(step):
        elem = world.browser.find_element_by_link_text(name)
        elem.click()


@step('I should see a link with the url "(.*?)"$')
def should_see_link(step, link_url):
    assert_true(step, world.browser.
                find_element_by_xpath(str('//a[@href="%s"]' % link_url)))


@step('I should see a link to "(.*?)" with the url "(.*?)"$')
def should_see_link_text(step, link_text, link_url):
    assert_true(step,
                world.browser.find_element_by_xpath(str(
                    '//a[@href="%s"][./text()="%s"]' %
                    (link_url, link_text))))


@step('I should see a link that contains the text "(.*?)" '
      'and the url "(.*?)"$')
def should_include_link_text(step, link_text, link_url):
    return world.browser.find_element_by_xpath(str(
        '//a[@href="%s"][contains(., %s)]' %
        (link_url, link_text)))


## General
@step('The element with id of "(.*?)" contains "(.*?)"$')
def element_contains(step, element_id, value):
    return world.browser.find_element_by_xpath(str(
        'id("{id}")[contains(text(), "{value}")]'.format(
            id=element_id, value=value)))


@step('The element with id of "(.*?)" does not contain "(.*?)"$')
def element_not_contains(step, element_id, value):
    elem = world.browser.find_elements_by_xpath(str(
        'id("{id}")[contains(text(), "{value}")]'.format(
            id=element_id, value=value)))
    assert_false(step, elem)


@step(r'I should see an element with id of "(.*?)" within (\d+) seconds?$')
def should_see_id_in_seconds(step, element_id, timeout):
    elem = wait_for_elem(world.browser, 'id("%s")' % element_id,
                         int(timeout))
    assert_true(step, elem)
    elem = elem[0]
    assert_true(step, elem.is_displayed())


@step('I should see an element with id of "(.*?)"$')
def should_see_id(step, element_id):
    elem = world.browser.find_element_by_xpath(str('id("%s")' % element_id))
    assert_true(step, elem.is_displayed())


@step('I should not see an element with id of "(.*?)"$')
def should_not_see_id(step, element_id):
    try:
        elem = world.browser.find_element_by_xpath(str('id("%s")' %
                                                   element_id))
        assert_true(step, not elem.is_displayed())
    except NoSuchElementException:
        pass


@step(r'I should see "([^"]+)" within (\d+) seconds?$')
def should_see_in_seconds(step, text, timeout):
    wait_for_content(step, world.browser, text, int(timeout))


@step('I should see "([^"]+)"$')
def should_see(step, text):
    assert_true(step, contains_content(world.browser, text))


@step('I see "([^"]+)"$')
def see(step, text):
    assert_true(step, contains_content(world.browser, text))


@step('I should not see "([^"]+)"$')
def should_not_see(step, text):
    assert_true(step, not contains_content(world.browser, text))


@step('I should be at "(.*?)"$')
def url_should_be(step, url):
    assert_true(step, url == world.browser.current_url)


## Browser
@step('The browser\'s URL should be "(.*?)"$')
def browser_url_should_be(step, url):
    assert_true(step, url == world.browser.current_url)


@step('The browser\'s URL should contain "(.*?)"$')
def url_should_contain(step, url):
    assert_true(step, url in world.browser.current_url)


@step('The browser\'s URL should not contain "(.*?)"$')
def url_should_not_contain(step, url):
    assert_true(step, url not in world.browser.current_url)


## Forms
@step('I should see a form that goes to "(.*?)"$')
def see_form(step, url):
    return world.browser.find_element_by_xpath(str('//form[@action="%s"]' %
                                                   url))


@step('I fill in "(.*?)" with "(.*?)"$')
def fill_in_textfield(step, field_name, value):
    with AssertContextManager(step):
        text_field = find_field(world.browser, 'text', field_name) or \
            find_field(world.browser, 'textarea', field_name) or \
            find_field(world.browser, 'password', field_name) or \
            find_field(world.browser, 'datetime', field_name) or \
            find_field(world.browser, 'datetime-local', field_name) or \
            find_field(world.browser, 'date', field_name) or \
            find_field(world.browser, 'month', field_name) or \
            find_field(world.browser, 'time', field_name) or \
            find_field(world.browser, 'week', field_name) or \
            find_field(world.browser, 'number', field_name) or \
            find_field(world.browser, 'range', field_name) or \
            find_field(world.browser, 'email', field_name) or \
            find_field(world.browser, 'url', field_name) or \
            find_field(world.browser, 'search', field_name) or \
            find_field(world.browser, 'tel', field_name) or \
            find_field(world.browser, 'color', field_name)
        assert_false(step, text_field is False,
                     'Can not find a field named "%s"' % field_name)
        text_field.clear()
        text_field.send_keys(value)


@step('I press "(.*?)"$')
def press_button(step, value):
    with AssertContextManager(step):
        button = find_button(world.browser, value)
        button.click()


@step('I click on label "([^"]*)"')
def click_on_label(step, label):
    """
    Click on a label
    """

    with AssertContextManager(step):
        elem = world.browser.find_element_by_xpath(str(
            '//label[normalize-space(text()) = "%s"]' % label))
        elem.click()


@step(r'Element with id "([^"]*)" should be focused')
def element_focused(step, id):
    """
    Check if the element is focused
    """

    elem = world.browser.find_element_by_xpath(str('id("{id}")'.format(id=id)))
    focused = world.browser.switch_to_active_element()

    assert_true(step, elem == focused)


@step(r'Element with id "([^"]*)" should not be focused')
def element_not_focused(step, id):
    """
    Check if the element is not focused
    """

    elem = world.browser.find_element_by_xpath(str('id("{id}")'.format(id=id)))
    focused = world.browser.switch_to_active_element()

    assert_false(step, elem == focused)


@step(r'Input "([^"]*)" (?:has|should have) value "([^"]*)"')
def input_has_value(step, field_name, value):
    """
    Check that the form input element has given value.
    """
    with AssertContextManager(step):
        text_field = find_field(world.browser, 'text', field_name) or \
            find_field(world.browser, 'textarea', field_name) or \
            find_field(world.browser, 'password', field_name)
        assert_false(step, text_field is False,
                     'Can not find a field named "%s"' % field_name)
        assert_equals(text_field.get_attribute('value'), value)


@step(r'I submit the only form')
def submit_the_only_form(step):
    """
    Look for a form on the page and submit it.
    """
    form = world.browser.find_element_by_xpath(str('//form'))
    form.submit()


@step(r'I submit the form with id "([^"]*)"')
def submit_form_id(step, id):
    """
    Submit the form having given id.
    """
    form = world.browser.find_element_by_xpath(str('id("{id}")'.format(id=id)))
    form.submit()


@step(r'I submit the form with action "([^"]*)"')
def submit_form_action(step, url):
    """
    Submit the form having given action URL.
    """
    form = world.browser.find_element_by_xpath(str('//form[@action="%s"]' %
                                                   url))
    form.submit()


# Checkboxes
@step('I check "(.*?)"$')
def check_checkbox(step, value):
    with AssertContextManager(step):
        check_box = find_field(world.browser, 'checkbox', value)
        if not check_box.is_selected():
            check_box.click()


@step('I uncheck "(.*?)"$')
def uncheck_checkbox(step, value):
    with AssertContextManager(step):
        check_box = find_field(world.browser, 'checkbox', value)
        if check_box.is_selected():
            check_box.click()


@step('The "(.*?)" checkbox should be checked$')
def assert_checked_checkbox(step, value):
    check_box = find_field(world.browser, 'checkbox', value)
    assert_true(step, check_box.is_selected())


@step('The "(.*?)" checkbox should not be checked$')
def assert_not_checked_checkbox(step, value):
    check_box = find_field(world.browser, 'checkbox', value)
    assert_true(step, not check_box.is_selected())


# Selectors
@step('I select "(.*?)" from "(.*?)"$')
def select_single_item(step, option_name, select_name):
    with AssertContextManager(step):
        option_box = find_option(world.browser, select_name, option_name)
        option_box.click()


@step('I select the following from "([^"]*?)":?$')
def select_multi_items(step, select_name):
    with AssertContextManager(step):
        # Ensure only the options selected are actually selected
        option_names = step.multiline.split('\n')
        select_box = find_field(world.browser, 'select', select_name)

        select = Select(select_box)
        select.deselect_all()

        for option in option_names:
            try:
                select.select_by_value(option)
            except NoSuchElementException:
                select.select_by_visible_text(option)


@step('The "(.*?)" option from "(.*?)" should be selected$')
def assert_single_selected(step, option_name, select_name):
    option_box = find_option(world.browser, select_name, option_name)
    assert_true(step, option_box.is_selected())


@step('The following options from "([^"]*?)" should be selected:?$')
def assert_multi_selected(step, select_name):
    with AssertContextManager(step):
        # Ensure its not selected unless its one of our options
        option_names = step.multiline.split('\n')
        select_box = find_field(world.browser, 'select', select_name)
        option_elems = select_box.find_elements_by_xpath(str('./option'))
        for option in option_elems:
            if option.get_attribute('id') in option_names or \
               option.get_attribute('name') in option_names or \
               option.get_attribute('value') in option_names or \
               option.text in option_names:
                assert_true(step, option.is_selected())
            else:
                assert_true(step, not option.is_selected())


@step(r'I should see option "([^"]*)" in selector "([^"]*)"')
def select_contains(step, option, id_):
    assert_true(step, option_in_select(world.browser, id_, option) is not None)


@step(r'I should not see option "([^"]*)" in selector "([^"]*)"')
def select_does_not_contain(step, option, id_):
    assert_true(step, option_in_select(world.browser, id_, option) is None)


## Radios
@step('I choose "(.*?)"$')
def choose_radio(step, value):
    with AssertContextManager(step):
        box = find_field(world.browser, 'radio', value)
        box.click()


@step('The "(.*?)" option should be chosen$')
def assert_radio_selected(step, value):
    box = find_field(world.browser, 'radio', value)
    assert_true(step, box.is_selected())


@step('The "(.*?)" option should not be chosen$')
def assert_radio_not_selected(step, value):
    box = find_field(world.browser, 'radio', value)
    assert_true(step, not box.is_selected())


# Alerts
@step('I accept the alert')
def accept_alert(step):
    """
    Accept the alert
    """

    try:
        alert = Alert(world.browser)
        alert.accept()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I dismiss the alert')
def dismiss_alert(step):
    """
    Dismiss the alert
    """

    try:
        alert = Alert(world.browser)
        alert.dismiss()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step(r'I should see an alert with text "([^"]*)"')
def check_alert(step, text):
    """
    Check the alert text
    """

    try:
        alert = Alert(world.browser)
        assert_equals(alert.text, text)
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I should not see an alert')
def check_no_alert(step):
    """
    Check there is no alert
    """

    try:
        alert = Alert(world.browser)
        raise AssertionError("Should not see an alert. Alert '%s' shown." %
                             alert.text)
    except NoAlertPresentException:
        pass


# Tooltips
@step(r'I should see an element with tooltip "([^"]*)"')
def see_tooltip(step, tooltip):
    """
    Press a button having a given tooltip.
    """
    elem = world.browser.find_elements_by_xpath(str(
        '//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)))
    elem = [e for e in elem if e.is_displayed()]
    assert_true(step, elem)


@step(r'I should not see an element with tooltip "([^"]*)"')
def no_see_tooltip(step, tooltip):
    """
    Press a button having a given tooltip.
    """
    elem = world.browser.find_elements_by_xpath(str(
        '//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)))
    elem = [e for e in elem if e.is_displayed()]
    assert_true(step, not elem)


@step(r'I (?:click|press) the element with tooltip "([^"]*)"')
def press_by_tooltip(step, tooltip):
    """
    Press a button having a given tooltip.
    """
    with AssertContextManager(step):
        for button in world.browser.find_elements_by_xpath(str(
            '//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
                dict(tooltip=tooltip))):
            try:
                button.click()
                break
            except Exception:
                pass


@step(r'The page title should be "([^"]*)"')
def page_title(step, title):
    """
    Check that the page title matches the given one.
    """

    with AssertContextManager(step):
        assert_equals(world.browser.title, title)


@step(r'I switch to the frame with id "([^"]*)"')
def switch_to_frame(self, frame):
    elem = world.browser.find_element_by_id(frame)
    world.browser.switch_to_frame(elem)


@step(r'I switch back to the main view')
def switch_to_main(self):
    world.browser.switch_to_default_content()
