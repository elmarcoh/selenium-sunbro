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
