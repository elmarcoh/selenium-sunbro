from selenium import webdriver
import os
import unittest

ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_PAGE = 'file://' + os.path.join(ROOT, 'test_page.html')

class TestCase(unittest.TestCase):
    """ Base test case """

    def setUp(self):
        driver_var = os.environ.get('WEBDRIVER', 'phantomjs').lower()
        if driver_var == 'firefox':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.PhantomJS()

    def tearDown(self):
        self.driver.quit()
