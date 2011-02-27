"""Utility functions that combine steps to locate elements"""

def element_id_by_label(browser, label):
    """Return the id of a label's for attribute"""
    for_id = browser.find_elements_by_xpath('//label[contains(., "%s")]' % label)
    if not for_id:
        return False
    return for_id[0].get_attribute('for')


## Field helper functions to locate select, textarea, and the other
## types of input fields (text, checkbox, radio)
def field_xpath(field, attribute):
    if field == 'select':
        return '//select[@%s="%%s"]' % attribute
    elif field == 'textarea':
        return '//textarea[@%s="%%s"]' % attribute
    else:
        return '//input[@%s="%%s"][@type="%s"]' % (attribute, field)


def find_field(browser, field, value):
    """Locate an input field of a given value
    
    This first looks for the value as the id of the element, then
    the name of the element, then a label for the element.
    
    """
    return find_field_by_id(browser, field, value) or \
        find_field_by_name(browser, field, value) or \
        find_field_by_label(browser, field, value)


def find_field_by_id(browser, field, id):
    xpath = field_xpath(field, 'id')
    elems = browser.find_elements_by_xpath(xpath % id)
    return elems[0] if elems else False


def find_field_by_name(browser, field, name):
    xpath = field_xpath(field, 'name')
    elems = browser.find_elements_by_xpath(xpath % name)
    return elems[0] if elems else False


def find_field_by_label(browser, field, label):
    """Locate the control input that has a label pointing to it
    
    This will first locate the label element that has a label of the given
    name. It then pulls the id out of the 'for' attribute, and uses it to
    locate the element by its id.
    
    """
    for_id = element_id_by_label(browser, label)
    if not for_id:
        return False
    return find_field_by_id(browser, field, for_id)
