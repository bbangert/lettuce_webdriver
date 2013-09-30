import os
import unittest
from functools import wraps

from lettuce import world
from lettuce.core import Feature

from lettuce_webdriver.tests import html_pages

PAGES = {}
for filename in os.listdir(html_pages):
    name = filename.split('.html')[0]
    PAGES[name] = 'file://%s' % os.path.join(html_pages, filename)


def feature(passed=None, failed=0, skipped=0):
    """
    Decorate a test method to test the feature contained in its docstring.

    Apply the context returned by the method to the feature.

    For example:
        @feature(passed=3)
        def test_some_feature(self):
            '''
            Feature: This name is returned
                Scenario: ...
                    When I {variable}
            '''

            return dict(variable=something)
    """

    assert passed is not None

    def outer(func):
        @wraps(func)
        def inner(self):
            import lettuce_webdriver.webdriver

            v = func(self)
            f = Feature.from_string(func.__doc__.format(**v))
            feature_result = f.run()
            scenario_result = feature_result.scenario_results[0]

            try:
                self.assertEquals(len(scenario_result.steps_passed), passed)
                self.assertEquals(len(scenario_result.steps_failed), failed)
                self.assertEquals(len(scenario_result.steps_skipped), skipped)
            except AssertionError:
                print "Failed", scenario_result.steps_failed
                if scenario_result.steps_failed:
                    print scenario_result.steps_failed[-1].why.traceback
                print "Skipped", scenario_result.steps_skipped
                print world.browser.page_source

                raise

        return inner

    return outer


class TestUtil(unittest.TestCase):
    def setUp(self):
        # Go to an empty page
        world.browser.get('')

    @feature(passed=5)
    def test_I_should_see(self):
        """
Feature: I should see, I should not see
    Scenario: Everything fires up
        When I visit "{page}"
        Then I should see "Hello there!"
        And I should see a link to "Google" with the url "http://google.com/"
        And I should see a link with the url "http://google.com/"
        And I should not see "Bogeyman"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=3)
    def test_I_see_a_link(self):
        """
Feature: I should see a link
    Scenario: Everything fires up
        When I go to "{page}"
        Then  I should see a link to "Google" with the url "http://google.com/"
        And I see "Hello there!"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=3)
    def test_see_a_link_containing(self):
        """
Feature: I should see a link containing
    Scenario: Everything fires up
        When I go to "{page}"
        Then The browser's URL should contain "file://"
        And I should see a link that contains the text "Goo" and the url "http://google.com/"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=6)
    def test_basic_page_linking(self):
        """
Feature: Basic page linking
    Scenario: Follow links
        Given I go to "{link_page}"
        And I see "Page o link"
        When I click "Next Page"
        Then I should be at "{link_dest_page}"
        And The browser's URL should be "{link_dest_page}"
        And The browser's URL should not contain "http://"
        """

        return {
            'link_page': PAGES['link_page'],
            'link_dest_page': PAGES['link_dest']
        }

    @feature(passed=4)
    def test_I_see_a_form(self):
        """
Feature: I should see a form
    Scenario: Everything fires up
        When I go to "{page}"
        Then I should see a form that goes to "basic_page.html"
        And the element with id of "somediv" contains "Hello"
        And the element with id of "somediv" does not contain "bye"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=5)
    def test_I_fill_in_a_form(self):
        """
Feature: I fill in a form
    Scenario: Everything fires up
        Given I go to "{page}"
        And I fill in "bio" with "everything awesome"
        And I fill in "Password: " with "neat"
        When I press "Submit!"
        Then The browser's URL should contain "bio=everything"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=4)
    def test_checkboxes_checked(self):
        """
Feature: Checkboxes checked
    Scenario: Everything fires up
        Given I go to "{page}"
        When I check "I have a bike"
        Then The "I have a bike" checkbox should be checked
        And The "I have a car" checkbox should not be checked
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=5)
    def test_checkboxes_unchecked(self):
        """
Feature: Checkboxes unchecked
    Scenario: Everything fires up
        Given I go to "{page}"
        And I check "I have a bike"
        And The "I have a bike" checkbox should be checked
        When I uncheck "I have a bike"
        Then The "I have a bike" checkbox should not be checked
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=6)
    def test_combo_boxes(self):
        """
Feature: Combo boxes
    Scenario: Everything fires up
        Given I go to "{page}"
        Then I should see option "Mercedes" in selector "car_choice"
        And I should see option "Volvo" in selector "car_choice"
        And I should not see option "Skoda" in selector "car_choice"
        When I select "Mercedes" from "car_choice"
        Then The "Mercedes" option from "car_choice" should be selected
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=1, failed=1)
    def test_combo_boxes_fail(self):
        """
Feature: Combo boxes fail
    Scenario: Everything fires up
        Given I go to "{page}"
        Then I should not see option "Mercedes" in selector "car_choice"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=3)
    def test_multi_combo_boxes(self):
        '''
Feature: Multi-combo-boxes
    Scenario: Everything fires up
        Given I go to "{page}"
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
        '''

        return dict(page=PAGES['basic_page'])

    @feature(passed=4)
    def test_radio_buttons(self):
        """
Feature: Radio buttons
    Scenario: Everything fires up
        When I go to "{page}"
        And I choose "Male"
        Then The "Male" option should be chosen
        And The "Female" option should not be chosen
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=4, failed=1, skipped=0)
    def test_hidden_text(self):
        """
Feature: Hidden text
    Scenario: Everything fires up
        When I go to "{page}"
        Then I should see an element with id of "bio_field"
        And I should see an element with id of "somediv" within 2 seconds
        And I should not see an element with id of "hidden_text"
        And I should see "Weeeee" within 1 second
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=2, failed=1, skipped=1)
    def test_hidden_text_2(self):
        """
Feature: Hidden text 2
    Scenario: Everything fires up
        When I go to "{page}"
        Then I should see "Hello there" within 1 second
        And I should see an element with id of "oops_field" within 1 second
        And I should not see an element with id of "hidden_text"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=5)
    def test_alert_accept(self):
        """
Feature: test alert accept
    Scenario: alerts
        When I go to "{page}"
        Then I should see an alert with text "This is an alerting alert"
        When I accept the alert
        Then I should not see an alert
        And I should see "true"
        """

        return dict(page=PAGES['alert_page'])

    @feature(passed=5)
    def test_alert_dismiss(self):
        """
Feature: test alert accept
    Scenario: alerts
        When I go to "{page}"
        Then I should see an alert with text "This is an alerting alert"
        When I dismiss the alert
        Then I should not see an alert
        And I should see "false"
        """

        return dict(page=PAGES['alert_page'])

    @feature(passed=6)
    def test_tooltips(self):
        """
Feature: test tooltips
    Scenario: tooltips
        When I go to "{page}"
        Then I should see an element with tooltip "A tooltip"
        And I should not see an element with tooltip "Does not exist"
        And I should not see an element with tooltip "Hidden"
        When I click the element with tooltip "A tooltip"
        Then the browser's URL should contain "#anchor"
        """

        return dict(page=PAGES['tooltips'])

    @feature(passed=4)
    def test_labels(self):
        """
Feature: test labels
    Scenario: basic page
        When I go to "{page}"
        And I click on label "Favorite Colors:"
        Then element with id "fav_colors" should be focused
        And element with id "bio_field" should not be focused
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=2, failed=1)
    def test_labels_fail(self):
        """
Feature: test labels fail
    Scenario: basic page
        When I go to "{page}"
        And I click on label "Favorite Colors:"
        Then element with id "fav_colors" should not be focused
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=3)
    def test_input_values(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        And I fill in "username" with "Danni"
        Then input "username" has value "Danni"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=2, failed=1)
    def test_input_values_fail(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        And I fill in "username" with "Danni"
        Then input "username" has value "Ricky"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=2)
    def test_page_title(self):
        """
Feature: assert value
    Scenario: basic page
        When I go to "{page}"
        Then the page title should be "A Basic Page"
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=4)
    def test_submit_only(self):
        """
Feature: submit only form
    Scenario: basic page
        When I go to "{page}"
        And I submit the only form
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=4)
    def test_submit_action(self):
        """
Feature: submit only form
    Scenario: basic page
        When I go to "{page}"
        And I submit the form with action "basic_page.html"
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="
        """

        return dict(page=PAGES['basic_page'])

    @feature(passed=4)
    def test_submit_id(self):
        """
Feature: submit only form
    Scenario: basic page
        When I go to "{page}"
        And I submit the form with id "the-form"
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="
        """

        return dict(page=PAGES['basic_page'])
