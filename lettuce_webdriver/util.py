"""Utility functions that combine steps to locate elements"""
def find_by_id(browser, field, id):
    return browser.find_element_by_xpath('//%s[@id=%s]' % (field, id))

def find_by_name(browser, field, name):
    return browser.find_element_by_xpath('//%s[@name=%s]' % (field, name))

def find_by_label(browser, label):
    for_id = browser.find_element_by_xpath('//label[@for=%s]' % label)
    assert for_id
    return find_by_id(browser, for_id)
