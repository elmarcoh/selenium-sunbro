from selenium.webdriver.common.by import By


class Selector:
    """Base selector"""
    pass


class FindElement(Selector):
    """Abstraction for selenium find_element"""

    def __init__(self, by, value):
        self._by = by
        self._value = value

    def find(self, element):
        """Performs the actual search.

        `element` is a driver or WebElement"""
        #import pdb; pdb.set_trace()
        return element.find_element(self._by, self._value)


def decorated_find(key):
    def getter(self):
        return getattr(self, key).find(self.driver)
    return getter


class PageMetaclass(type):
    """Metaclass that search for selenium selector objects on the
    class and makes them usable on the Page object
    """

    def __new__(cls, classname, bases, attrs):
        final_attrs = {}
        for k, v in attrs.iteritems():
            if isinstance(v, Selector):
                _k = '_' + k
                final_attrs[_k] = v
                final_attrs[k] = property(decorated_find(_k))
            else:
                final_attrs[k] = v

        return type.__new__(cls, classname, bases, final_attrs)


class Page:
    __metaclass__ = PageMetaclass

    def __init__(self, driver):
        self.driver = driver
