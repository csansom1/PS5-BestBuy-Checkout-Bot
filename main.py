from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from random import randint, randrange
import time
import info
import random

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
BEST_BUY_URL = "https://www.bestbuy.ca/en-ca/product/playstation-5-console/15689336"
BEST_BUY_TEST_URL = "https://www.bestbuy.ca/en-ca/product/the-legend-of-zelda-link-s-awakening-switch/12601646"
WAIT_TIME = 5


class PS5BestBuyBot:
	def __init__(self, username, password, cvv):
		self.username = username
		self.password = password
		self.cvv = cvv
		options = Options()
		options.add_argument('--disable-blink-features=AutomationControlled')
		self.driver = webdriver.Chrome(DRIVER_PATH, options=options)

	## Sign into site with the product
	def signIn(self):
		""" Sign into site with the product. """
		driver = self.driver  ## Navigate to URL

		## Enter Username
		username_elem = driver.find_element_by_xpath("//input[@name='username']")
		username_elem.clear()
		username_elem.send_keys(self.username)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## Enter Password
		password_elem = driver.find_element_by_xpath("//input[@name='password']")
		password_elem.clear()
		password_elem.send_keys(self.password)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		password_elem.send_keys(Keys.RETURN)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

	## Find product under X amount
	def findProduct(self):
		""" Finds the product with global link. """
		driver = self.driver
		#driver.get(BEST_BUY_TEST_URL)
		driver.get(BEST_BUY_URL)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## If the product is not available, wait until it is available
		is_available = self.isProductAvailable()

		while is_available == 'Coming soon':
			#driver.get(BEST_BUY_TEST_URL)
			driver.get(BEST_BUY_URL)
			time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
			is_available = self.isProductAvailable()

		## Restart browser if access denied
		if is_available == "Access denied":
			self.closeBrowser()
			time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
			options = Options()
			options.add_argument('--disable-blink-features=AutomationControlled')
			self.driver = webdriver.Chrome(DRIVER_PATH, options=options)
			self.findProduct()
			return

		## Add to cart
		add_to_cart = driver.find_element_by_class_name('addToCartButton')
		add_to_cart.click()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## View cart
		view_cart = driver.find_element_by_class_name('viewCart')
		view_cart.click()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## Continue to checkout
		continue_to_checkout = driver.find_element_by_class_name('continueToCheckout_3Dgpe')
		continue_to_checkout.click()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		self.signIn()
		time.sleep(8)

		## Confirm CVV
		cvv_field = driver.find_element_by_xpath("//input[@name='cvv']")
		cvv_field.clear()
		cvv_field.send_keys(self.cvv)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## Place Order
		place_order = driver.find_element_by_class_name('order-now')
		#place_order_type = place_order.get_attribute('type')
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		#print(f'***** PLACE ORDER: {place_order_type}')
		place_order.click()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		button = driver.driver.find_element_by_xpath("//input[@type='button']")
		button.send_keys(Keys.RETURN)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		print(f'***** ORDER PLACED')

	def isProductAvailable(self):
		""" Checks if product is available. """
		driver = self.driver
		try:
			availability = driver.find_element_by_class_name('availabilityMessage_ig-s5').text
			print(f'***** AVAILABILITY: {availability}')
			return availability
		except NoSuchElementException:
			print('***** ACCESS DENIED')
			return "Access denied"

	def closeBrowser(self):
		""" Closes browser """
		print(f'***** CLOSE BROWSER')
		self.driver.close()


if __name__ == '__main__':
	shopBot = PS5BestBuyBot(username=info.username, password=info.password, cvv=info.cvv)
	shopBot.findProduct()
	shopBot.closeBrowser()
