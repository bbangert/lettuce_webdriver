"""Webdriver support for lettuce"""
from lettuce import step
from lettuce import world

from lettuce_webdriver.util import find_field
from lettuce_webdriver.util import find_field_by_id
from lettuce_webdriver.util import find_field_by_name
from lettuce_webdriver.util import find_field_by_label


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


## Browser
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


@step('The browser\'s URL should be "(.*?)"')
def browser_url_should_be(step, url):
    assert url == world.browser.current_url


@step ('The browser\'s URL should contain "(.*?)"')
def url_should_contain(step, url):
    assert url in world.browser.current_url


@step ('The browser\'s URL should not contain "(.*?)"')
def url_should_not_contain(step, url):
    assert url not in world.browser.current_url

