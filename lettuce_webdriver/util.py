"""Utility functions that combine steps to locate elements"""
from nose.tools import assert_true as nose_assert_true
from nose.tools import assert_false as nose_assert_false

class AssertContextManager():
    def __init__(self, step):
        self.step = step

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        step = self.step
        if traceback:
            if isinstance(value, AssertionError):
                error = AssertionError(self.step.sentence)
            else:
                sentence = "%s, failed because: %s" % (step.sentence, value)
                error = AssertionError(sentence)
            raise error, None, traceback 

def assert_true(step, exp):
    with AssertContextManager(step):
        nose_assert_true(exp)

def assert_false(step, exp, msg=None):
    with AssertContextManager(step):
        nose_assert_false(exp, msg)

def element_id_by_label(browser, label):
    """Return the id of a label's for attribute"""
    for_id = browser.find_elements_by_xpath('//label[contains(., "%s")]' % label)
    if not for_id:
        return False
    return for_id[0].get_attribute('for')


## Field helper functions to locate select, textarea, and the other
## types of input fields (text, checkbox, radio)
def field_xpath(field, attribute):
    if field in ['select', 'textarea']:
        return './/%s[@%s="%%s"]' % (field, attribute)
    elif field == 'button':
        if attribute == 'value':
            return './/%s[contains(., "%%s")]' % (field, )
        else:
            return './/%s[@%s="%%s"]' % (field, attribute)
    elif field == 'option':
        return './/%s[@%s="%%s"]' % (field, attribute)
    else:
        return './/input[@%s="%%s"][@type="%s"]' % (attribute, field)


def find_button(browser, value):
    return find_field_with_value(browser, 'submit', value) or \
        find_field_with_value(browser, 'reset', value) or \
        find_field_with_value(browser, 'button', value) or \
        find_field_with_value(browser, 'image', value)


def find_field_with_value(browser, field, value):
    return find_field_by_id(browser, field, value) or \
        find_field_by_name(browser, field, value) or \
        find_field_by_value(browser, field, value)


def find_option(browser, select_name, option_name):
    # First, locate the select
    select_box = find_field(browser, 'select', select_name)
    assert select_box
    
    # Now locate the option
    option_box = find_field(select_box, 'option', option_name)
    if not option_box:
        # Locate by contents
        option_box = select_box.find_element_by_xpath('./option[contains(., "%s")]' % option_name)
    return option_box


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


def find_field_by_value(browser, field, name):
    xpath = field_xpath(field, 'value')
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
