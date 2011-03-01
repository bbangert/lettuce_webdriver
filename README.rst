=============================================
Lettuce steps for Web Testing with Selenium 2
=============================================

``lettuce_webdriver`` provides a set of steps for use with the `Cucumber
<http://cukes.info/>`_ BDD Python port `lettuce <http://lettuce.it/>`_ using
the `selenium 2.0b2 Python package <http://pypi.python.org/pypi/selenium>`_.

The included matchers and syntax is inspired heavily by `cucumber_watir
<https://github.com/napcs/cucumber_watir>`_.

Requirements
============

* `lettuce <http://lettuce.it/>`_
* `selenium 2.0b2 <http://pypi.python.org/pypi/selenium>`_

Setting Up lettuce_webdriver
============================

In your lettuce ``terrain.py`` file, add an include statement for lettuce to
learn about the additional step definitions provided by
``lettuce_webdriver`` and a setup that creates the selenium browser
desired::
    
    from lettuce import before, world
    from selenium import webdriver
    import lettuce_webdriver.webdriver
    
    @before.all
    def setup_browser():
        world.browser = webdriver.Firefox()

Usage
=====

lettuce stories are written in the standard Cucumber style of `gherkin
<https://github.com/aslakhellesoy/cucumber/wiki/gherkin>`_. For example::
    
    Scenario: Filling out the signup form
      Given I go to "http://foo.com/signup"
       When I fill in "Name" with "Foo Bar"
        And I fill in "Email" with "nospam@gmail.com"
        And I fill in "City" with "San Jose"
        And I fill in "State" with "CA"
        And I uncheck "Send me spam!"
        And I select "Male" from "Gender"
        And I press "Sign up"
       Then I should see "Thank you for signing up!"


Included Matchers
-----------------

The following lettuce step matchers are included in this package and can be
used with Given/When/Then/And as desired.

::

    # urls
    I visit "http://google.com/"
    I go to "http://google.com/"
    
    # links
    I click "Next page"
    I should see a link with the url "http://foobar.com/"
    I should see a link to "Google" with the url "http://google.com/"
    I should see a link that contains the text "Foobar" and the url "http://foobar.com/"

    # general
    I should see "Page Content"
    I see "Page Content"
    I should not see "Foobar"
    I should be at "http://foobar.com/"
    I should see an element with id of "http://bar.com/"
    I should not see an element with id of "http://bar.com/"
    The element with id of "cs_PageModeContainer" contains "Read"
    The element with id of "cs_BigDiv" does not contain "Write"

    # browser
    The browser's URL should be "http://bar.com/"
    The browser's URL should contain "foo.com"
    The browser's URL should not contain "bar.com"
    
    # forms
    I should see a form that goes to "http://bar.com/submit.html"
    I press "Submit"
    
    # checkboxes
    I check "I have a car"
    I uncheck "I have a bus"
    The "I have a car" checkbox should be checked
    The "I have a bus" checkbox should not be checked
    
    # select
    I select "Volvo" from "Car Choices"
    I select the following from "Car Choices":
        """
        Volvo
        Saab
        """
    The "Volvo" option from "Car Choices" should be selected
    The following options from "Car Choices" should be selected:
        """
        Volvo
        Saab
        """
    
    # radio buttons
    I choose "Foobar"
    The "Foobar" option should be chosen
    The "Bar" option should not be chosen
    
    # text entry fields (text, textarea, password)
    I fill in "Username" with "Smith"
