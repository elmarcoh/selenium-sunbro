import sunbro
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest


class YapoAdInsertPage(sunbro.Page):
    form = sunbro.FindByName('formular')
    subject = sunbro.FindByCSS('input#subject', within='form')
    body = sunbro.FindByName('body')
    price = sunbro.FindByName('price', within='form')
    titles = sunbro.FindAllByCSS('.title')

    advice = sunbro.FindElement(By.CSS_SELECTOR, 'ul.type1')

    def go(self):
        self._driver.get('http://www2.yapo.cl/ai')


class TestSimplePageObject(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def tearDown(self):
        self.driver.quit()

    def test_form_fill(self):
        page = YapoAdInsertPage(self.driver)
        page.go()
        page.subject.send_keys('Praise the sun, bros!')
        page.body.send_keys('...to summon one another as'
                            ' spirits, cross the gaps between'
                            ' the worlds, and engage in jolly co-operation!')
        page.price.send_keys('1231')

    def test_get_selector(self):
        page = YapoAdInsertPage(None)
        self.assertEqual(('css selector', 'input#subject'),
                         page.selector('subject'))

    def test_get_old_selector(self):
        page = YapoAdInsertPage(None)
        self.assertEqual(('css selector', 'ul.type1'), page.selector('advice'))
