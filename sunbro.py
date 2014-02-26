import sys
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
        return element.find_element(self._by, self._value)


class MetaFinder(type):
    """Selenium selector metaclass"""

    def __init__(cls, classname, bases, attrs):

        by = attrs.pop('_by')

        def find(self, root_element):
            return root_element.find_element(by, self._value)

        def init(self, value):
            self._value = value

        attrs['__init__'] = init
        attrs['find'] = find
        return type.__init__(cls, classname, (Selector,) + bases, attrs)


FindByClassName = MetaFinder('FindByClassName', (), {'_by': By.CLASS_NAME})
FindByCSS = MetaFinder('FindByCSS', (), {'_by': By.CSS_SELECTOR})
FindById = MetaFinder('FindById', (), {'_by': By.ID})
FindByLinkText = MetaFinder('FindByLinkText', (), {'_by': By.LINK_TEXT})
FindByName = MetaFinder('FindByName', (), {'_by': By.NAME})
FindByPartialLinkText = MetaFinder('FindByPartialLinkText', (), {'_by': By.PARTIAL_LINK_TEXT})
FindByTag = MetaFinder('FindByTag', (), {'_by': By.TAG_NAME})
FindByXPath = MetaFinder('FindByXPath', (), {'_by': By.XPATH})


def decorated_find(key):
    def getter(self):
        return getattr(self, key).find(self._driver)
    return getter


class BasePage(object):
    def __init__(self, driver):
        self._driver = driver


class PageMetaclass(type):
    """Metaclass that search for selenium selector objects on the
    class and makes them usable on the Page object
    """

    def __new__(cls, classname, bases, attrs):
        final_attrs = {}

        if sys.version < '3':
            items = attrs.iteritems()
        else:
            items = iter(attrs.items())

        for k, v in items:
            if isinstance(v, Selector):
                _k = '_' + k
                final_attrs[_k] = v
                final_attrs[k] = property(decorated_find(_k))
            else:
                final_attrs[k] = v

        return type.__new__(cls, classname, bases, final_attrs)


Page = PageMetaclass('Page', (BasePage, ), {})


#class Page:
#    """Extend this class to generate page objects.
#
#    By adding Selector as attributes, web elements will be lazy loaded
#    as you request them as properties
#    """
#    __metaclass__ = PageMetaclass
#
#    def __init__(self, driver):
#        """
#        driver: selenium.webdriver
#        """
#        self.driver = driver
