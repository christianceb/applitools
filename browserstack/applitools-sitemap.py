# Iterates through a sitemap of a site provided you know a unique parent container that houses these sitemap links. Visits the links 1 by 1 and takes a screenshot for comparison or testing in Applitools.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from applitools.eyes import Eyes
from applitools.common import StitchMode

class Website:
  enable_eyes = True

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
        test_name='Website Test - Sitemap'
      )

    domain = '' # put the url to test here.

    # Get Home
    driver.get(domain)
    
    # Create snapshot for frontpage.
    if enable_eyes: eyes.check_window('Frontpage')

    print('Frontpage')

    # Sitemap (get contents). Pretty known that sitemaps of sites are in <domain>/sitemap
    driver.get(domain + 'sitemap')

    # Create snapshot for Sitemap
    if enable_eyes: eyes.check_window('Sitemap')

    print('Sitemap')

    sites = []

    # Collect href and text of anchors in sitemap before we move away from the current window
    for element in driver.find_elements_by_css_selector('.sitemap a'):
      if element.text != 'Sitemap':
        sites.append({
          'href': element.get_attribute('href'),
          'text': element.text
        })

    # Loop through the collected links earlier and snapshot them
    for site in sites:
      driver.get( site['href'] )
      if enable_eyes: eyes.check_window( site['text'] )
      print(site['text'])

    # Close Eyes
    if enable_eyes: eyes.close()
  finally:
    # End the tests
    driver.quit()

    if enable_eyes: eyes.abort_if_not_closed()