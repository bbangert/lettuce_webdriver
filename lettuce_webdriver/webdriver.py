"""Webdriver support for lettuce"""
from lettuce import step
from lettuce import world

from lettuce_webdriver.util import find_button
from lettuce_webdriver.util import find_field
from lettuce_webdriver.util import find_field_by_id
from lettuce_webdriver.util import find_field_by_name
from lettuce_webdriver.util import find_field_by_label
from lettuce_webdriver.util import find_option


## URLS
@step('I visit "(.*?)"')
def visit(step, url):
    world.browser.get(url)

@step('I go to "(.*?)"')
def goto(step, url):
    world.browser.get(url)


## Links
@step('I click "(.*?)"')
def click(step, name):
    elem = world.browser.find_element_by_link_text(name)
    elem.click()


@step('I should see a link with the url "(.*?)"')
def should_see_link(step, link_url):
    assert world.browser.find_element_by_xpath('//a[@href="%s"]' % link_url)


@step('I should see a link to "(.*?)" with the url "(.*?)"')
def should_see_link_text(step, link_text, link_url):
    assert world.browser.find_element_by_xpath('//a[@href="%s"][./text()="%s"]' %
        (link_url, link_text))


@step('I should see a link that contains the text "(.*?)" and the url "(.*?)"')
def should_include_link_text(step, link_text, link_url):
    return world.browser.find_element_by_xpath('//a[@href="%s"][contains(., %s)]' % 
        (link_url, link_text))


## General
@step('The element with id of "(.*?)" contains "(.*?)"')
def element_contains(step, element_id, value):
    return world.browser.find_element_by_xpath('//*[@id="%s"][contains(., "%s")]' %
        (element_id, value))

@step('I should see "([^"]+)"')
def should_see(step, text):
    assert text in world.browser.get_page_source()


@step('I see "([^"]+)"')
def see(step, text):
    assert text in world.browser.get_page_source()


@step('I should not see "([^"]+)"')
def should_not_see(step, text):
    assert text not in world.browser.get_page_source()


@step('I should be at "(.*?)"')
def url_should_be(step, url):
    assert url == world.browser.current_url


## Browser
@step('The browser\'s URL should be "(.*?)"')
def browser_url_should_be(step, url):
    assert url == world.browser.current_url


@step ('The browser\'s URL should contain "(.*?)"')
def url_should_contain(step, url):
    assert url in world.browser.current_url


@step ('The browser\'s URL should not contain "(.*?)"')
def url_should_not_contain(step, url):
    assert url not in world.browser.current_url


## Forms
@step('I should see a form that goes to "(.*?)"')
def see_form(step, url):
    return world.browser.find_element_by_xpath('//form[@action="%s"]' % url)


@step('I fill in "(.*?)" with "(.*?)"')
def fill_in_textfield(step, field_name, value):
    text_field = find_field(world.browser, 'text', field_name) or \
        find_field(world.browser, 'textarea', field_name) or \
        find_field(world.browser, 'password', find_field)
    text_field.clear()
    text_field.send_keys(value)


@step('When I press "(.*?)"')
def press_button(step, value):
    button = find_button(world.browser, value)
    button.click()


@step('I check "(.*?)"')
def check_checkbox(step, value):
    check_box = find_field(world.browser, 'checkbox', value)
    check_box.select()


@step('I uncheck "(.*?)"')
def uncheck_checkbox(step, value):
    check_box = find_field(world.browser, 'checkbox', value)
    if check_box.is_selected():
        check_box.toggle()


@step('The "(.*?)" checkbox should be checked')
def assert_checked_checkbox(step, value):
    check_box = find_field(world.browser, 'checkbox', value)
    assert check_box.is_selected()


@step('The "(.*?)" checkbox should not be checked')
def assert_not_checked_checkbox(step, value):
    check_box = find_field(world.browser, 'checkbox', value)
    assert not check_box.is_selected()


@step('I select "(.*?)" from "(.*?)"')
def select_single_item(step, option_name, select_name):
    option_box = find_option(world.browser, select_name, option_name)
    option_box.select()


@step('The "(.*?)" option from "(.*?)" should be selected')
def assert_single_selected(step, option_name, select_name):
    option_box = find_option(world.browser, select_name, option_name)
    assert option_box.is_selected()


@step('The "(.*?)" option from "(.*?)" should not be selected')
def assert_single_selected(step, option_name, select_name):
    option_box = find_option(world.browser, select_name, option_name)
    assert not option_box.is_selected()


@step('I choose "(.*?)"')
def choose_radio(step, value):
    box = find_field(world.browser, 'radio', value)
    box.select()


@step('The "(.*?)" option should be chosen')
def assert_radio_selected(step, value):
    box = find_field(world.browser, 'radio', value)
    assert box.is_selected()


@step('The "(.*?)" option should not be chosen')
def assert_radio_selected(step, value):
    box = find_field(world.browser, 'radio', value)
    assert not box.is_selected()
