# Simple way to test a couple of site's pages and its modal window functionalities by simulating mouse clicks.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from applitools.eyes import Eyes
from applitools.common import StitchMode

class Website:
  enable_eyes = False

  # Establish Eyes
  if enable_eyes:
    eyes = Eyes()
    eyes.api_key = ''
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
      command_executor='',
      desired_capabilities=caps
    )

    # Maximize Window
    driver.maximize_window()

    # Define the test
    if enable_eyes:
      eyes.open(
        driver=driver,
        app_name='Website',
        test_name='Website Test - Modal Form'
      )

    domain = '' # put the url to test here.

    # Get Home
    driver.get(domain)
    # Create snapshot for frontpage.
    if enable_eyes: eyes.check_window('Frontpage')
    print('Frontpage')
    
    # frontpage listing modal
    driver.find_elements_by_css_selector('.career-listing:first-child a.apply-online-link').click() # open listing modal
    if enable_eyes: eyes.check_window('Frontpage (career listing modal open)')
    print('Frontpage (career listing modal open)')
    driver.find_elements_by_css_selector('.apply-lightbox .form .close-lightbox').click() # close listing modal

    # frontpage 'get in touch' modal
    driver.find_elements_by_css_selector('.get-in-touch-button').click() # open get in touch modal
    if enable_eyes: eyes.check_window('Frontpage (get in touch modal open)')
    print('Frontpage (get in touch modal open)')
    # no need to close modal, we're moving away anyway.

    # get career single post
    driver.get(domain + 'careers/account-supervisor-social-and-digital-experience/')
    if enable_eyes: eyes.check_window('Career Single Post')
    print('Career Single Post')

    # career single post apply modal
    driver.find_elements_by_css_selector('.career-apply .apply-online-button').click() # open apply modal
    if enable_eyes: eyes.check_window('Career Single Post Apply Modal')
    print('Career Single Post Apply Modal')
    # no need to close modal, we're moving away anyway.

    # Close Eyes
    if enable_eyes: eyes.close()
  finally:
    # End the tests
    driver.quit()

    if enable_eyes: eyes.abort_if_not_closed()