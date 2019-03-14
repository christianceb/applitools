# Simple way of regression testing a static html site using Selenium Webdriver, Applitools (remote), and Bootstrap elements.
# To detect changes after you have made a baseline by simply running this code, modify index.html and rerun this script.
#
# Note that this tests locally and not with BrowserStack. You will need to make sure that Selenium WebDriver is installed properly.
# Also ensure that you have Chrome WebDriver work properly. This is a VERY BASIC test: if you can't make it run on this code, you can't do this properly anywhere else (especially BrowserStack!)

from selenium import webdriver
from applitools.eyes import Eyes
class Bootstrap:
  eyes = Eyes()

  eyes.api_key = '' # Enter your "API" key here from applitools.

  try:
    driver = webdriver.Chrome()

    eyes.open(
      driver=driver,
      app_name='Bootstrap',
      test_name='Selenium Python Test',
      viewport_size={'width': 1024, 'height': 640}
    )

    driver.get('index.html')

    eyes.check_window('Load')

    eyes.close()
  finally:
    driver.quit()

    eyes.abort_if_not_closed()