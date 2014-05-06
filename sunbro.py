"""Handy module to create page objects.

Sunbro is a module that allows the creation of page objects in a declarative
way, so when wiriting tests you only have to worry about wiriting the actual
test, instead of tricky selectors.

Usage:
    Page object classes must inherit from sunbro.Page class, and selectors
    should be sublasses of Find.

class MyAwesomePage(sunbro.Page):
    title = sunbro.FindByTag('h1')
    tricky_css = sunbro.FindByCSS('div.tricky p')
    link = sunbro.FindByID('linky')


page = MyAwesomePage.link.click()
"""

import sys
from selenium.webdriver.common.by import By


class Find(object):
    def __init__(self, selector, within=None):
        self._selector = selector
        self._within = within


#TODO find metods should only receive the root element and work it's way
#     through the hierarchy

class FindElements(Find):
    """Abstraction for selenium find_elements"""

    def __init__(self, by, value):
        self._by = by
        self._value = value

    def find(self, element):
        """Performs the actual search.

        `element` is a driver or WebElement"""
        return element.find_elements(self._by, self._value)


class FindElement(Find):
    """Abstraction for selenium find_element"""

    def __init__(self, by, value):
        self._by = by
        self._value = value

    def find(self, element):
        """Performs the actual search.

        `element` is a driver or WebElement"""
        return element.find_element(self._by, self._value)


class MetaFind(type):
    """Selenium selector metaclass"""

    def __new__(cls, classname, bases, attrs):

        by = attrs.pop('_by')

        def find(self, root):
            return root.find_element(by, self._selector)

        attrs['find'] = find
        return type.__new__(cls, classname, (Find,) + bases, attrs)


class MetaFindAll(type):
    """Selenium selector metaclass"""

    def __new__(cls, classname, bases, attrs):

        by = attrs.pop('_by')

        def find(self, root_element):
            return root_element.find_elements(by, self._selector)

        attrs['find'] = find
        return type.__new__(cls, classname, (Find,) + bases, attrs)

selectors = {
    'Class': By.CLASS_NAME,
    'CSS': By.CSS_SELECTOR,
    'ID': By.ID,
    'LinkText': By.LINK_TEXT,
    'Name': By.NAME,
    'PartialLinkText': By.PARTIAL_LINK_TEXT,
    'Tag': By.TAG_NAME,
    'XPath': By.XPATH,
}

for name, by in selectors.items():
    classname = 'FindBy' + name
    selclass = MetaFind(classname, (), {'_by': by})
    vars()[classname] = selclass
    classname = 'FindAllBy' + name
    selclass = MetaFindAll(classname, (), {'_by': by})
    vars()[classname] = selclass


def decorated_find(finder):
    def getter(self):
        driver = self._driver
        if finder._within:
            root = getattr(self, finder._within)
        else:
            root = driver
        return finder.find(root)
    return getter


class BasePage(object):
    """Base page for page objects, you should not extend from this, use Page instead"""
    def __init__(self, driver):
        self._driver = driver

    def fill_fields(self, **kwargs):
        """Fills the fields referenced by kwargs keys and fill them with the value"""
        for name, value in kwargs.items():
            field = getattr(self, name)
            field.send_keys(value)

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
            if isinstance(v, Find):
                final_attrs[k] = property(decorated_find(v))
            else:
                final_attrs[k] = v

        return type.__new__(cls, classname, bases, final_attrs)


Page = PageMetaclass('Page', (BasePage, ), {})
Page.__doc__ = "Base class for page objects"
