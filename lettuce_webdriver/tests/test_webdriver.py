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

FEATURE5 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        When I go to "%(page)s"
        Then I should see a form that goes to "basic_page.html"
        And The element with id of "somediv" contains "Hello"
        And The element with id of "somediv" does not contain "bye"
""" % {'page': PAGES['basic_page']}

FEATURE6 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        Given I go to "%(page)s"
        And I fill in "bio" with "everything awesome"
        And I fill in "Password: " with "neat"
        When I press "Submit!"
        Then The browser's URL should contain "bio=everything"
""" % {'page': PAGES['basic_page']}

FEATURE7 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        Given I go to "%(page)s"
        When I check "I have a bike"
        Then The "I have a bike" checkbox should be checked
        And The "I have a car" checkbox should not be checked
""" % {'page': PAGES['basic_page']}

FEATURE8 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        Given I go to "%(page)s"
        And I check "I have a bike"
        And The "I have a bike" checkbox should be checked
        When I uncheck "I have a bike"
        Then The "I have a bike" checkbox should not be checked
""" % {'page': PAGES['basic_page']}

FEATURE9 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        Given I go to "%(page)s"
        When I select "Mercedes" from "car_choice"
        Then The "Mercedes" option from "car_choice" should be selected
""" % {'page': PAGES['basic_page']}


FEATURE10 = '''
Feature: Basic page formstuff
    Scenario: Everything fires up
        Given I go to "%(page)s"
        When I select the following from "Favorite Colors:":
            """
            Blue
            Green
            """
        Then The following options from "Favorite Colors:" should be selected:
            """
            Blue
            Green
            """
''' % {'page': PAGES['basic_page']}


FEATURE11 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        When I go to "%(page)s"
        And I choose "Male"
        Then The "Male" option should be chosen
        And The "Female" option should not be chosen
""" % {'page': PAGES['basic_page']}


FEATURE12 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        When I go to "%(page)s"
        Then I should see an element with id of "bio_field"
        And I should see an element with id of "somediv" within 2 seconds
        And I should not see an element with id of "hidden_text"
        And I should see "Weeeee" within 1 second
""" % {'page': PAGES['basic_page']}


FEATURE13 = """
Feature: Basic page formstuff
    Scenario: Everything fires up
        When I go to "%(page)s"
        Then I should see "Hello there" within 1 second
        And I should see an element with id of "oops_field" within 1 second
        And I should not see an element with id of "hidden_text"
""" % {'page': PAGES['basic_page']}


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

    def test_feature5(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE5)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 4)

    def test_feature6(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE6)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 5)

    def test_feature7(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE7)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 4)

    def test_feature8(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE8)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 5)

    def test_feature9(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE9)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 3)

    def test_feature10(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE10)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 3)

    def test_feature11(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE11)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 4)

    def test_feature12(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE12)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 4)

    def test_feature13(self):
        import lettuce_webdriver.webdriver
        f = Feature.from_string(FEATURE13)
        feature_result = f.run()
        scenario_result = feature_result.scenario_results[0]
        self.assertEquals(len(scenario_result.steps_passed), 2)
