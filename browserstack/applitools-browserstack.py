# Simple regression testing of a frontpage using Selenium and processing results to Applitools.

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from applitools.eyes import Eyes
from applitools.common import StitchMode

class Bootstrap:
  enable_eyes = True

  # Initialize Eyes
  if enable_eyes:
    eyes = Eyes()
    eyes.api_key = '' # your API key on Applitools, explained on an earlier chapter.
    eyes.force_full_page_screenshot = True
    
    # Force stitching of screenshots on pages where floating elements might appear twice on the screenshot
    # Note that this functionality is not perfect and fails miserably on a sticky header that resizes later in the scroll.
    eyes.stitch_mode = StitchMode.CSS

  # Configure Chrome
  options = webdriver.ChromeOptions()
  options.add_argument("--disable-infobars")
  caps = options.to_capabilities()
  
  desired_cap = {
    'browser': 'Chrome',
    'browser_version': '62.0',
    'os': 'Windows',
    'os_version': '10',
    'resolution': '1920x1080'
  }

  # Merge Chrome Settings
  caps.update(desired_cap)

  try:
    # Setup WebDriver object to access remote device.
    driver = webdriver.Remote(
      command_executor='', # your "API Key" on BrowserStack.
      desired_capabilities=caps
    )

    # Maximize Window
    driver.maximize_window()

    # Define the test
    if enable_eyes:
      eyes.open(
        driver=driver,
        app_name='Bootstrap',
        test_name='Selenium Python Test'
      )

    driver.get('') # put the url to test here.
    
    if enable_eyes: eyes.check_window('Load')

    # Close Eyes
    if enable_eyes: eyes.close()
  finally:
    # End the tests
    driver.quit()

    if enable_eyes: eyes.abort_if_not_closed()