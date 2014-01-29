import sunbro
from selenium import webdriver

class GoogleSearchPage(sunbro.Page):
    subject = sunbro.FindElement('name', 'subject')
    body = sunbro.FindElement('name', 'body')
    price = sunbro.FindElement('name', 'price')

    def go(self):
        self.driver.get('http://www2.yapo.cl/ai')


if __name__ == '__main__':
    driver = webdriver.Firefox()
    page = GoogleSearchPage(driver)
    page.go()
    page.subject.send_keys('ola k ase')
    page.body.send_keys('soy un space marine')
    page.price.send_keys('1231')
