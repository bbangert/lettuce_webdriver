"""Webdriver support for lettuce"""
from lettuce import step
from lettuce import world

from lettuce_webdriver import find_by_id
from lettuce_webdriver import find_by_name
from lettuce_webdriver import find_by_label


## Links
@step('I visit "([^"]+)"')
@step('I go to "([^"]+)"')
def goto(step, url):
    world.browser.get(url)

@step('I click "([^"]+)"')
def click(step, name):
    elem = world.browser.find_element_by_link_text(name)
    elem.click()

@step('I should see "([^"]+)"')
@step('I see "([^"]+)"')
def should_see(step, text):
    assert text in world.browser.get_page_source()

@step('I should not see "([^"]+)"')
def should_see(step, text):
    assert text not in world.browser.get_page_source()

@step('I should see a link with the url "(.*?)"')
def should_see_link(step, link_url):
    assert world.browser.find_element_by_xpath('//a[@href="%s"]' % link_url)

@step('I should see a link to "(.*?)" with the url "(.*?)"')
def should_see_link_text(step, link_text, link_url):
    assert world.browser.find_element_by_xpath('//a[@href="%s"][./text()="%s"]' %
        (link_url, link_text))

