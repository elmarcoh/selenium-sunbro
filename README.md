Selenium SunBro
===============

Sunbro is a module aimed to ease the creation of Page Objects by allowing them to be written in a declarative way, similar to the way models and forms are written in the django web framework.

	import sunbro
	from selenium import webdriver

	class YapoAdInsertPage(sunbro.Page):
		subject = sunbro.FindElement('name', 'subject')
		body = sunbro.FindElement('name', 'body')
		price = sunbro.FindElement('name', 'price')

		def go(self):
			self.driver.get('http://www2.yapo.cl/ai')


	if __name__ == '__main__':
		driver = webdriver.Firefox()
		page = YapoAdInsertPage(driver)
		page.go()
		page.subject.send_keys('Praise the sun, bros!')
		page.body.send_keys('...to summon one another as spirits, cross the gaps between the worlds, and engage in jolly co-operation!')
		page.price.send_keys('1231')


Why sunbro?
http://darksouls.wiki.fextralife.com/Warrior+of+Sunlight
