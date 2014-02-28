import sunbro
from selenium import webdriver


class YapoAdInsertPage(sunbro.Page):
    form = sunbro.FindByName('formular')
    subject = sunbro.FindByCSS('input#subject', within='form')
    body = sunbro.FindByName('body')
    price = sunbro.FindByName('price')
    titles = sunbro.FindAllByCSS('.title')

    def go(self):
        self._driver.get('http://www2.yapo.cl/ai')


if __name__ == '__main__':
    driver = webdriver.Firefox()
    page = YapoAdInsertPage(driver)
    page.go()
    page.subject.send_keys('Praise the sun, bros!')
    page.body.send_keys('...to summon one another as'
                        ' spirits, cross the gaps between'
                        ' the worlds, and engage in jolly co-operation!')
    page.price.send_keys('1231')
