from sunbro.selectors import Select
import os
import sunbro
from . import TestCase

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestPage(sunbro.Page):
    select = Select(css='select')

    def go(self):
        self._driver.get('file://' + os.path.join(ROOT, 'test_page.html'))


class TestSimplePageObject(TestCase):

    def test_select_by_value(self):
        """The <select> web element is correctly wrapped"""
        page = TestPage(self.driver)
        page.go()
        page.select.select_by_value('2')
        selected = page.select.first_selected_option
        assert selected.text == 'Second'
