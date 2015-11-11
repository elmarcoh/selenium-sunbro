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

from selenium.webdriver.common.by import By


class Find(object):
    def __init__(self, selector, within=None):
        self._selector = selector
        self._within = within


# TODO find metods should only receive the root element and work it's way
#     through the hierarchy

class FindElements(Find):
    """Abstraction for selenium find_elements"""

    def __init__(self, by, selector):
        self._by = by
        super(FindElements, self).__init__(selector)

    def find(self, element):
        """Performs the actual search.

        `element` is a driver or WebElement"""
        return element.find_elements(self._by, self._selector)


class FindElement(Find):
    """Abstraction for selenium find_element"""

    def __init__(self, by, selector):
        self._by = by
        super(FindElement, self).__init__(selector)

    def find(self, element):
        """Performs the actual search.

        `element` is a driver or WebElement"""
        return element.find_element(self._by, self._selector)


class MetaFind(type):
    """Selenium selector metaclass"""

    def __new__(cls, classname, bases, attrs):

        def find(self, root):
            return root.find_element(self._by, self._selector)

        attrs['find'] = find
        return type.__new__(cls, classname, (Find,) + bases, attrs)


class MetaFindAll(type):
    """Selenium selector metaclass"""

    def __new__(cls, classname, bases, attrs):

        def find(self, root_element):
            return root_element.find_elements(self._by, self._selector)

        attrs['find'] = find
        return type.__new__(cls, classname, (Find,) + bases, attrs)

By.IOS_UIAUTOMATION = '-ios uiautomation'
By.ANDROID_UIAUTOMATOR = '-android uiautomator'
By.ACCESSIBILITY_ID = 'accessibility id'

selectors = {
    'Class': By.CLASS_NAME,
    'CSS': By.CSS_SELECTOR,
    'ID': By.ID,
    'LinkText': By.LINK_TEXT,
    'Name': By.NAME,
    'PartialLinkText': By.PARTIAL_LINK_TEXT,
    'Tag': By.TAG_NAME,
    'XPath': By.XPATH,
    'IosUiAutomator' : By.IOS_UIAUTOMATION,
    'AndroidUiAutomator' : By.ANDROID_UIAUTOMATOR,
    'AccessibilityId' : By.ACCESSIBILITY_ID,
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
    """Base page for page objects, you should not extend from this,
       use Page instead"""
    def __init__(self, driver):
        self._driver = driver

    def fill_fields(self, **kwargs):
        """Fills the fields referenced by kwargs keys and fill them with
        the value"""
        for name, value in kwargs.items():
            field = getattr(self, name)
            field.send_keys(value)

    def selector(self, fieldname):
        """Gets a selector for the given page element as a tuple
        (by, selector)"""
        finder = self._finders[fieldname]
        return (finder._by, finder._selector)


class PageMetaclass(type):
    """Metaclass that search for selenium selector objects on the
    class and makes them usable on the Page object
    """

    def __new__(cls, classname, bases, attrs):
        finders = {}
        for k, v in [i for i in attrs.items() if isinstance(i[1], Find)]:
            if isinstance(v, Find):
                attrs[k] = property(decorated_find(v))
                finders[k] = v

        attrs['_finders'] = finders
        return type.__new__(cls, classname, bases, attrs)


Page = PageMetaclass('Page', (BasePage, ), {})
Page.__doc__ = "Base class for page objects"
