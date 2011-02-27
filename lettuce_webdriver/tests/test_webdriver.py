import os
import unittest

from lettuce import world
from lettuce.core import Feature

from lettuce_webdriver.tests import html_pages

PAGES = {}
for filename in os.listdir(html_pages):
    name = filename.split('.html')[0]
    PAGES[name] = 'file://%s' % os.path.join(html_pages, filename)


FEATURE1 = """
Feature: Basic page loads
    Scenario: Everything fires up
        When I visit "%s"
        Then I should see "Hello there!"
        And I should see a link to "Google" with the url "http://google.com/"
        And I should see a link with the url "http://google.com/"
        And I should not see "Bogeyman"
""" % PAGES['basic_page']

FEATURE2 = """
Feature: Basic page loads
    Scenario: Everything fires up
        When I go to "%s"
        Then  I should see a link to "Google" with the url "http://google.com/"
        And I see "Hello there!"
""" % PAGES['basic_page']

FEATURE3 = """
Feature: Basic page loads
    Scenario: Everything fires up
        When I go to "%(page)s"
        Then The browser's URL should contain "file://"
        And I should see a link that contains the text "Goo" and the url "http://google.com/"
""" % {'page': PAGES['basic_page']}

FEATURE4 = """
Feature: Basic page linking
    Scenario: Follow links
        Given I go to "%(link_page)s"
        And I see "Page o link"
        When I click "Next Page"
        Then I should be at "%(link_dest_page)s"
        And The browser's URL should be "%(link_dest_page)s"
        And The browser's URL should not contain "http://"
""" % {'link_page': PAGES['link_page'],
       'link_dest_page': PAGES['link_dest']}


class TestUtil(unittest.TestCase):
    def setUp(self):
        # Go to an empty page
        world.browser.get('')

    def test_feature1(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE1)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 5)

    def test_feature2(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE2)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 3)

    def test_feature3(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE3)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 3)

    def test_feature4(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE4)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 6)
