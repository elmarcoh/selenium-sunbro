from selenium.webdriver.support.select import Select as SeleniumSelect
from selenium.webdriver.common.by import By
from exceptions import NotImplementedError
from sunbro import FindElement

# TODO: This is redundant with the list on __init__.py
selectors = {
    'class': By.CLASS_NAME,
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'link_text': By.LINK_TEXT,
    'name': By.NAME,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'xpath': By.XPATH,
}


class FindAndWrap(FindElement):
    """ Finds an element and wraps it using the `wrap` method"""

    def __init__(self, **kwargs):
        selector_type, selector = (None, None)
        for key, val in kwargs.items():
            if key in selectors:
                selector_type = key
                selector = val
                break
        by = selectors.get(selector_type)
        super(FindAndWrap, self).__init__(by, selector)

    def find(self, top):
        """Searches for the element and wraps it"""
        elem = super(FindAndWrap, self).find(top)
        return self.wrap(elem)

    def wrap(self, elem):
        """Wraps an element

        Derived classes must implement this method in order for it to work
        """
        raise NotImplementedError("`wrap` is not implemented on this class")


class Select(FindAndWrap):

    def wrap(self, elem):
        """Wraps an element as a select"""
        return SeleniumSelect(elem)
