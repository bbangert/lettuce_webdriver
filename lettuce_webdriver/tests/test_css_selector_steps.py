import os
import unittest

from lettuce import world
from lettuce.core import Feature

from lettuce_webdriver.tests import html_pages

PAGES = {}
for filename in os.listdir(html_pages):
    name = filename.split('.html')[0]
    PAGES[name] = 'file://%s' % os.path.join(html_pages, filename)


FEATURES = [
    """
    Feature: Wait and match CSS
        Scenario: Everything fires up
            When I go to "%(page)s"
            Then There should be an element matching $("textarea[name='bio']") within 1 second
    """ % {'page': PAGES['basic_page']},

    """
    Feature: CSS-based formstuff
        Scenario: Everything fires up
            When I go to "%(page)s"
            Then I fill in $("input[name='user']") with "A test string"
            And I check $("input[value='Bike']")
    """ % {'page': PAGES['basic_page']},    
]

class TestUtil(unittest.TestCase):
    def setUp(self):
        # Go to an empty page
        world.browser.get('')

    def test_features(self):
        import lettuce_webdriver.webdriver
        import lettuce_webdriver.css_selector_steps
        for feature_string in FEATURES:
            f = Feature.from_string(feature_string)
            feature_result = f.run()
            scenario_result = feature_result.scenario_results[0]
            self.assertFalse(scenario_result.steps_failed)
            self.assertFalse(scenario_result.steps_skipped)
            self.assertFalse(scenario_result.steps_undefined)
