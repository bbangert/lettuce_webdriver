import os

from lettuce import world

here = os.path.dirname(__file__)
html_pages = os.path.join(here, 'html_pages')

def setUp():
    from selenium import webdriver
    world.browser = webdriver.Firefox()

def tearDown():
    world.browser.quit()
