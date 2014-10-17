"""Utility functions that combine steps to locate elements"""

import operator
import time

from itertools import chain

from selenium.common.exceptions import NoSuchElementException

from nose.tools import assert_true as nose_assert_true
from nose.tools import assert_false as nose_assert_false

# pylint:disable=missing-docstring,redefined-outer-name,redefined-builtin
# pylint:disable=invalid-name


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


def assert_true(step, exp, msg=None):
    with AssertContextManager(step):
        nose_assert_true(exp, msg)


def assert_false(step, exp, msg=None):
    with AssertContextManager(step):
        nose_assert_false(exp, msg)


class Selector(object):
    """
    A set of elements on a page.

    Delays evaluation to batch the queries together, allowing operations on
    selectors (e.g. union) to be performed first, and then issuing as few
    requests to the browser as possible.

    Also behaves as a single element by proxying all method calls, asserting
    that there is only one element selected.
    """

    def __init__(self, browser):
        self.browser = browser

    def _select(self):
        """
        Fetch the elements from the browser.

        Override in subclasses.
        """
        raise NotImplementedError("Please override select().")

    def _elements(self):
        """
        The cached list of elements.
        """
        if not hasattr(self, '_elements_cached'):
            setattr(self, '_elements_cached', list(self._select()))
        return self._elements_cached

    # The class behaves as a container for the elements, fetching the list from
    # the browser on the first attempt to enumerate itself.

    def __len__(self):
        return len(self._elements())

    def __getitem__(self, key):
        return self._elements()[key]

    def __iter__(self):
        for el in self._elements():
            yield el

    def __nonzero__(self):
        return bool(self._elements())

    def __add__(self, other):
        """
        Return a union of the two selectors.

        Where possible, avoid evaluating either selector to batch queries.
        """

        if isinstance(other, RealisedSelector):
            # no better than a list
            other = list(other)

        if isinstance(other, Selector):
            return MultiSelector(self.browser, self, other)
        else:
            if not other:
                # Nothing to add
                return self

            # This will perform a query if other is a selector.
            try:
                other = list(other)
            except TypeError:
                other = [other]

            return RealisedSelector(self.browser,
                                    list(self) + other)

    def __getattr__(self, attr):
        """
        Delegate all calls to the only element selected.
        """

        if attr == '_elements_cached':
            # Never going to be on the element
            raise AttributeError()

        assert len(self) == 1, \
            'Must be a single element, have {0}'.format(len(self))
        return getattr(self[0], attr)


class RealisedSelector(Selector):
    """
    A selector specifying elements directly.
    """

    def __init__(self, browser, elements):
        super(RealisedSelector, self).__init__(browser)
        self.elements = elements

    def _select(self):
        return self.elements


class MultiSelector(Selector):
    """
    A selector adding up many selectors.
    """

    def __init__(self, browser, *selectors):
        super(MultiSelector, self).__init__(browser)
        self.selectors = selectors

    def _select(self):
        return chain.from_iterable(sel._select()
                                   for sel in self.selectors)

    def __add__(self, other):
        selectors = self.selectors
        if isinstance(other, MultiSelector):
            selectors += other.selectors
        else:
            selectors += (other,)
        return MultiSelector(self.browser, *selectors)


class XPathSelector(Selector):
    """
    An XPath selector.

    Several of these can be joined together so that only a single query is made
    to the browser.
    """

    def __init__(self, browser, xpath):
        super(XPathSelector, self).__init__(browser)
        self.xpath = xpath

    def _select(self):
        return self.browser.find_elements_by_xpath(self.xpath)

    def __add__(self, other):
        """
        If possible, return a single selector, avoiding evaluation.
        """

        if isinstance(other, XPathSelector):
            return XPathSelector(self.browser,
                                 self.xpath + '|' + other.xpath)
        else:
            return super(XPathSelector, self).__add__(other)


def sum1(values):
    """
    Add up all the values without specifying the initial element.
    """
    return reduce(operator.add, values)


def element_id_by_label(browser, label):
    """Return the id of a label's for attribute"""
    label = XPathSelector(browser,
                          str('//label[contains(., "%s")]' % label))
    if not label:
        return False
    return label.get_attribute('for')


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
    return find_field_with_value(browser, 'submit', value) + \
        find_field_with_value(browser, 'reset', value) + \
        find_field_with_value(browser, 'button', value) + \
        find_field_with_value(browser, 'image', value)


def find_field_with_value(browser, field, value):
    return find_field_by_id(browser, field, value) + \
        find_field_by_name(browser, field, value) + \
        find_field_by_value(browser, field, value)


def find_option(browser, select_name, option_name):
    # First, locate the select
    select_box = find_field(browser, 'select', select_name)
    assert select_box

    # Now locate the option
    option_box = find_field(select_box, 'option', option_name)
    if not option_box:
        # Locate by contents
        option_box = select_box.find_element_by_xpath(str(
            './/option[contains(., "%s")]' % option_name))
    return option_box


def find_field(browser, field, value):
    """Locate an input field of a given value

    This first looks for the value as the id of the element, then
    the name of the element, then a label for the element.

    """
    return find_field_by_id(browser, field, value) + \
        find_field_by_name(browser, field, value) + \
        find_field_by_label(browser, field, value)


def find_any_field(browser, field_types, field_name):
    """
    Find a field of any of the specified types.
    """

    return sum1(find_field(browser, field_type, field_name)
                 for field_type in field_types)


def find_field_by_id(browser, field, id):
    return XPathSelector(browser, field_xpath(field, 'id') % id)


def find_field_by_name(browser, field, name):
    return XPathSelector(browser, field_xpath(field, 'name') % name)


def find_field_by_value(browser, field, name):
    xpath = field_xpath(field, 'value')
    elems = [elem for elem in XPathSelector(browser, str(xpath % name))
             if elem.is_displayed() and elem.is_enabled()]

    # sort by shortest first (most closely matching)
    if field == 'button':
        elems = sorted(elems, key=lambda elem: len(elem.text))
    else:
        elems = sorted(elems,
                       key=lambda elem: len(elem.get_attribute('value')))

    return elems


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


def option_in_select(browser, select_name, option):
    """
    Returns the Element specified by @option or None

    Looks at the real <select> not the select2 widget, since that doesn't
    create the DOM until we click on it.
    """

    select = find_field(browser, 'select', select_name)
    assert select

    try:
        return select.find_element_by_xpath(str(
            './/option[normalize-space(text()) = "%s"]' % option))
    except NoSuchElementException:
        return None


def wait_for(func):
    """
    A decorator to invoke a function periodically until it returns a truthy
    value.
    """

    def wrapped(*args, **kwargs):
        timeout = kwargs.pop('timeout', 15)

        start = time.time()
        result = None

        while time.time() - start < timeout:
            result = func(*args, **kwargs)
            if result:
                break
            time.sleep(0.2)

        return result

    return wrapped
