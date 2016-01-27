import sunbro
from selenium.webdriver.common.by import By
from . import TestCase, TEST_PAGE


class SamplePage(sunbro.Page):
    form = sunbro.FindByID('form')
    subject = sunbro.FindByCSS('input#textbox', within='form')
    body = sunbro.FindByName('textarea')

    advice = sunbro.FindElement(By.CSS_SELECTOR, 'ul.type1')

    submit = sunbro.FindByCSS('button')

    def go(self):
        self._driver.get(TEST_PAGE)


class TestSimplePageObject(TestCase):

    def test_form_fill(self):
        page = SamplePage(self.driver)
        page.go()
        page.subject.send_keys('Praise the sun, bros!')
        page.body.send_keys('...to summon one another as'
                            ' spirits, cross the gaps between'
                            ' the worlds, and engage in jolly co-operation!')

        page.submit.click()

    def test_get_selector(self):
        page = SamplePage(None)
        self.assertEqual(('css selector', 'input#textbox'),
                         page.selector('subject'))

    def test_get_old_selector(self):
        page = SamplePage(None)
        self.assertEqual(('css selector', 'ul.type1'), page.selector('advice'))
